"""Tests for the astronomy observation game."""

import unittest
import time

from astronomy.sky import Sky, angular_distance
from astronomy.jobs import ObservationRequest, JobQueue
from astronomy.telescope import Telescope, noise_floor, radio_noise_floor, INSTRUMENTS
from astronomy.sessions import SessionStore


class TestAngularDistance(unittest.TestCase):

    def test_same_point(self):
        self.assertAlmostEqual(angular_distance(10, 20, 10, 20), 0.0)

    def test_known_distance(self):
        # Poles are 180 degrees apart
        self.assertAlmostEqual(angular_distance(0, 90, 0, -90), 180.0)

    def test_small_distance(self):
        d = angular_distance(42.5, 15.3, 42.8, 15.1)
        self.assertGreater(d, 0)
        self.assertLess(d, 1.0)


class TestNoiseModel(unittest.TestCase):

    def test_longer_exposure_lower_noise(self):
        imager = INSTRUMENTS["imager"]
        n1 = noise_floor(10, imager, "clear")
        n2 = noise_floor(300, imager, "clear")
        # Higher limiting magnitude = can see fainter = "lower noise"
        self.assertGreater(n2, n1)

    def test_narrowband_reduces_depth(self):
        imager = INSTRUMENTS["imager"]
        n_clear = noise_floor(60, imager, "clear")
        n_ha = noise_floor(60, imager, "h_alpha")
        # Narrow-band filter reduces overall depth
        self.assertGreater(n_clear, n_ha)

    def test_radio_noise_decreases_with_time(self):
        n1 = radio_noise_floor(10)
        n2 = radio_noise_floor(1000)
        self.assertGreater(n1, n2)


class TestSky(unittest.TestCase):

    def setUp(self):
        self.sky = Sky(seed=42)

    def test_catalogue_loaded(self):
        self.assertEqual(len(self.sky.objects), 12)

    def test_add_player(self):
        p = self.sky.add_player("test-session")
        self.assertIn("test-session", self.sky.players)
        self.assertTrue(0 <= p.ra <= 360)
        self.assertTrue(-90 <= p.dec <= 90)

    def test_objects_in_fov(self):
        # Lyrion Nebula is at ra=42.5, dec=15.3
        objs = self.sky.objects_in_fov(42.5, 15.3, 1.5)
        names = [o.name for o in objs]
        self.assertIn("Lyrion Nebula", names)
        self.assertIn("Kael's Star", names)

    def test_objects_not_in_fov(self):
        # Nothing near ra=180, dec=80
        objs = self.sky.objects_in_fov(180, 80, 1.0)
        self.assertEqual(len(objs), 0)

    def test_player_exclusion(self):
        self.sky.add_player("p1")
        self.sky.add_player("p2")
        p1 = self.sky.players["p1"]
        # Looking right at p1's location should find p2 only if nearby
        found = self.sky.players_in_fov(p1.ra, p1.dec, 360.0, exclude_session="p1")
        session_ids = [p.session_id for p in found]
        self.assertNotIn("p1", session_ids)
        self.assertIn("p2", session_ids)


class TestObservationRequest(unittest.TestCase):

    def test_valid_request(self):
        req = ObservationRequest(
            target_ra=42.5, target_dec=15.3,
            instrument="imager", filter_band="clear",
            exposure_time=60,
        )
        self.assertEqual(req.validate(), [])

    def test_invalid_ra(self):
        req = ObservationRequest(
            target_ra=400, target_dec=0,
            instrument="imager", filter_band=None,
            exposure_time=60,
        )
        errors = req.validate()
        self.assertTrue(any("ra" in e for e in errors))

    def test_invalid_instrument(self):
        req = ObservationRequest(
            target_ra=0, target_dec=0,
            instrument="laser_cannon", filter_band=None,
            exposure_time=60,
        )
        errors = req.validate()
        self.assertTrue(any("instrument" in e for e in errors))

    def test_exposure_too_long(self):
        req = ObservationRequest(
            target_ra=0, target_dec=0,
            instrument="imager", filter_band=None,
            exposure_time=9999,
        )
        errors = req.validate()
        self.assertTrue(any("exposure" in e for e in errors))


class TestJobQueue(unittest.TestCase):

    def test_submit_and_retrieve(self):
        q = JobQueue()
        req = ObservationRequest(0, 0, "imager", None, 60)
        job = q.submit("s1", req)
        self.assertEqual(job.status.value, "processing")
        retrieved = q.get_job(job.job_id)
        self.assertIs(retrieved, job)

    def test_session_jobs(self):
        q = JobQueue()
        req = ObservationRequest(0, 0, "imager", None, 60)
        q.submit("s1", req)
        q.submit("s1", req)
        q.submit("s2", req)
        self.assertEqual(len(q.get_session_jobs("s1")), 2)
        self.assertEqual(len(q.get_session_jobs("s2")), 1)


class TestTelescope(unittest.TestCase):

    def setUp(self):
        self.sky = Sky(seed=42)
        self.telescope = Telescope(self.sky, rng_seed=42)

    def test_image_observation_finds_objects(self):
        req = ObservationRequest(42.5, 15.3, "imager", "clear", 300)
        result = self.telescope.observe("test", req)
        self.assertIn("headers", result)
        self.assertIn("data", result)
        self.assertEqual(result["data"]["type"], "image")
        names = [d["name"] for d in result["data"]["detections"]]
        self.assertIn("Kael's Star", names)

    def test_radio_observation_finds_pulsar(self):
        req = ObservationRequest(128.7, -44.2, "radio_receiver", None, 300)
        result = self.telescope.observe("test", req)
        self.assertEqual(result["data"]["type"], "radio_map")
        names = [d["name"] for d in result["data"]["detections"]]
        self.assertIn("Vorantis Pulsar", names)

    def test_spectrograph_acquires_target(self):
        # Point right at Kael's Star
        req = ObservationRequest(42.8, 15.1, "spectrograph", "clear", 300)
        result = self.telescope.observe("test", req)
        self.assertEqual(result["data"]["type"], "spectrum")
        self.assertTrue(result["data"]["target_acquired"])
        self.assertEqual(result["data"]["spectrum_class"], "G")

    def test_spectrograph_empty_sky(self):
        req = ObservationRequest(180, 80, "spectrograph", "clear", 60)
        result = self.telescope.observe("test", req)
        self.assertFalse(result["data"]["target_acquired"])

    def test_fits_headers_present(self):
        req = ObservationRequest(0, 0, "imager", "r_band", 60)
        result = self.telescope.observe("test", req)
        h = result["headers"]
        self.assertTrue(h["SIMPLE"])
        self.assertEqual(h["RA"], 0.0)
        self.assertEqual(h["DEC"], 0.0)
        self.assertEqual(h["EXPTIME"], 60)
        self.assertEqual(h["FILTER"], "R_BAND")
        self.assertIn("DATE-OBS", h)
        self.assertIn("TELESCOP", h)

    def test_player_detection_optical(self):
        # Add another player near a known location
        self.sky.players["other"] = self.sky.add_player.__func__  # manual
        from astronomy.sky import PlayerSource
        self.sky.players["other"] = PlayerSource(
            session_id="other", ra=100.0, dec=20.0,
            optical_brightness=12.0,  # bright enough to detect easily
        )
        req = ObservationRequest(100.0, 20.0, "imager", "clear", 300)
        result = self.telescope.observe("test", req)
        kinds = [d["kind"] for d in result["data"]["detections"]]
        self.assertIn("unidentified", kinds)

    def test_player_detection_radio(self):
        from astronomy.sky import PlayerSource
        self.sky.players["other"] = PlayerSource(
            session_id="other", ra=100.0, dec=20.0,
            radio_flux=200.0,
        )
        req = ObservationRequest(100.0, 20.0, "radio_receiver", None, 300)
        result = self.telescope.observe("test", req)
        kinds = [d["kind"] for d in result["data"]["detections"]]
        self.assertIn("unidentified", kinds)

    def test_broadcast_increases_detectability(self):
        from astronomy.sky import PlayerSource
        self.sky.players["other"] = PlayerSource(
            session_id="other", ra=100.0, dec=20.0,
            radio_flux=5.0, broadcast_power=5.0,
        )
        req = ObservationRequest(100.0, 20.0, "radio_receiver", None, 60)
        result = self.telescope.observe("test", req)
        detections = result["data"]["detections"]
        player_det = [d for d in detections if d["kind"] == "unidentified"]
        self.assertTrue(len(player_det) > 0)
        self.assertEqual(player_det[0]["signal_character"], "narrowband")


class TestSessionStore(unittest.TestCase):

    def setUp(self):
        self.store = SessionStore()

    def test_create_session(self):
        session = self.store.create_session()
        self.assertIsNotNone(session.session_id)
        self.assertIn(session.session_id, self.store.sky.players)

    def test_submit_and_check_observation(self):
        session = self.store.create_session()
        req = ObservationRequest(42.5, 15.3, "imager", "clear", 60)
        job = self.store.submit_observation(session.session_id, req)
        self.assertEqual(job.status.value, "processing")

        # Force ready by backdating start time
        job.started_at = time.time() - 100
        checked = self.store.check_job(session.session_id, job.job_id)
        self.assertEqual(checked.status.value, "completed")
        self.assertIsNotNone(checked.result)

    def test_invalid_request_rejected(self):
        session = self.store.create_session()
        req = ObservationRequest(999, 0, "imager", None, 60)
        with self.assertRaises(ValueError):
            self.store.submit_observation(session.session_id, req)

    def test_transmit(self):
        session = self.store.create_session()
        result = self.store.transmit(session.session_id, 5.0)
        self.assertEqual(result["transmit_power"], 5.0)
        self.assertEqual(
            self.store.sky.players[session.session_id].broadcast_power, 5.0)

    def test_transmit_clamped(self):
        session = self.store.create_session()
        result = self.store.transmit(session.session_id, 999.0)
        self.assertEqual(result["transmit_power"], 10.0)


if __name__ == "__main__":
    unittest.main()
