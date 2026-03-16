"""Tests for the astronomy observation game."""

import unittest
import time

from astronomy.sky import Sky, PlayerSource, _angular_distance
from astronomy.jobs import ObservationRequest, JobQueue
from astronomy.telescope import Telescope, noise_floor, radio_noise_floor, INSTRUMENTS
from astronomy.sessions import SessionStore
from astronomy.physics import vec3_distance, position_to_apparent
from astronomy.regions import REGIONS, region_for_position


class TestAngularDistance(unittest.TestCase):

    def test_same_point(self):
        self.assertAlmostEqual(_angular_distance(10, 20, 10, 20), 0.0)

    def test_poles_apart(self):
        self.assertAlmostEqual(_angular_distance(0, 90, 0, -90), 180.0)

    def test_small_distance(self):
        d = _angular_distance(42.5, 15.3, 42.8, 15.1)
        self.assertGreater(d, 0)
        self.assertLess(d, 1.0)


class TestVec3(unittest.TestCase):

    def test_distance_same_point(self):
        p = {"x": 1.0, "y": 2.0, "z": 3.0}
        self.assertAlmostEqual(vec3_distance(p, p), 0.0)

    def test_distance_known(self):
        a = {"x": 0.0, "y": 0.0, "z": 0.0}
        b = {"x": 3.0, "y": 4.0, "z": 0.0}
        self.assertAlmostEqual(vec3_distance(a, b), 5.0)

    def test_position_to_apparent(self):
        obs = {"x": 0.0, "y": 0.0, "z": 0.0}
        src = {"x": 1.0, "y": 0.0, "z": 0.0}
        ra, dec, dist = position_to_apparent(obs, src)
        self.assertAlmostEqual(dist, 1.0)
        self.assertAlmostEqual(dec, 0.0, places=5)


class TestNoiseModel(unittest.TestCase):

    def test_longer_exposure_deeper(self):
        imager = INSTRUMENTS["imager"]
        n1 = noise_floor(10, imager, "clear")
        n2 = noise_floor(300, imager, "clear")
        self.assertGreater(n2, n1)

    def test_narrowband_reduces_depth(self):
        imager = INSTRUMENTS["imager"]
        n_clear = noise_floor(60, imager, "clear")
        n_ha = noise_floor(60, imager, "h_alpha")
        self.assertGreater(n_clear, n_ha)

    def test_radio_noise_decreases_with_time(self):
        n1 = radio_noise_floor(10)
        n2 = radio_noise_floor(1000)
        self.assertGreater(n1, n2)


class TestRegions(unittest.TestCase):

    def test_regions_exist(self):
        self.assertGreater(len(REGIONS), 0)

    def test_region_for_position(self):
        # Quiet Dark center
        r = region_for_position({"x": -0.02, "y": 0.015, "z": 0.005})
        self.assertIsNotNone(r)
        self.assertEqual(r.id, "quiet-dark")

    def test_no_region(self):
        r = region_for_position({"x": 100.0, "y": 100.0, "z": 100.0})
        self.assertIsNone(r)


class TestSky(unittest.TestCase):

    def setUp(self):
        self.sky = Sky(seed=42)

    def test_catalogue_loaded(self):
        self.assertEqual(len(self.sky.objects), 17)

    def test_add_player(self):
        p = self.sky.add_player("test-session")
        self.assertIn("test-session", self.sky.players)
        self.assertIn("x", p.position_au)
        self.assertIn("y", p.position_au)
        self.assertIn("z", p.position_au)

    def test_sources_in_fov(self):
        # Observer at origin, look toward Kael's Star position
        obs = {"x": 0.0, "y": 0.0, "z": 0.0}
        star_pos = {"x": -0.004, "y": 0.009, "z": 0.001}
        ra, dec, _ = position_to_apparent(obs, star_pos)
        results = self.sky.sources_in_fov(obs, ra, dec, 2.0)
        names = [obj.name for obj, *_ in results]
        self.assertIn("Kael's Star", names)

    def test_player_exclusion(self):
        self.sky.add_player("p1")
        self.sky.add_player("p2")
        p1 = self.sky.players["p1"]
        # Look toward p1's position from origin
        obs = {"x": 0.0, "y": 0.0, "z": 0.0}
        ra, dec, _ = position_to_apparent(obs, p1.position_au)
        found = self.sky.players_in_fov(obs, ra, dec, 180.0, exclude_session="p1")
        session_ids = [p.session_id for p, *_ in found]
        self.assertNotIn("p1", session_ids)
        self.assertIn("p2", session_ids)

    def test_player_physical_state(self):
        p = self.sky.add_player("test")
        self.assertGreater(p.power_draw, 0)
        self.assertEqual(p.stored_heat, 0.0)
        self.assertEqual(p.radiator_mode, "balanced")


class TestObservationRequest(unittest.TestCase):

    def test_valid_request(self):
        req = ObservationRequest(
            target_ra=42.5, target_dec=15.3,
            instrument="imager", filter_band="clear",
            exposure_time=60,
        )
        self.assertEqual(req.validate(), [])

    def test_valid_with_scan_profile(self):
        req = ObservationRequest(
            target_ra=0, target_dec=0,
            instrument="imager", filter_band=None,
            exposure_time=60, scan_profile="boosted",
        )
        self.assertEqual(req.validate(), [])

    def test_invalid_scan_profile(self):
        req = ObservationRequest(
            target_ra=0, target_dec=0,
            instrument="imager", filter_band=None,
            exposure_time=60, scan_profile="turbo",
        )
        errors = req.validate()
        self.assertTrue(any("scan_profile" in e for e in errors))

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

    def test_jump_job(self):
        q = JobQueue()
        dest = {"x": 0.01, "y": 0.0, "z": 0.0}
        job = q.submit_jump("s1", dest, "standard", 30.0, time.time())
        self.assertEqual(job.status.value, "processing")
        retrieved = q.get_jump_job(job.job_id)
        self.assertIs(retrieved, job)


class TestTelescope(unittest.TestCase):

    def setUp(self):
        self.sky = Sky(seed=42)
        self.telescope = Telescope(self.sky, rng_seed=42)
        # Add a test observer at origin
        self.sky.players["test"] = PlayerSource(
            session_id="test",
            position_au={"x": 0.0, "y": 0.0, "z": 0.0},
            last_tick=time.time(),
        )

    def test_image_observation_finds_objects(self):
        # Compute apparent RA/Dec of Kael's Star from origin
        star_pos = {"x": -0.004, "y": 0.009, "z": 0.001}
        ra, dec, _ = position_to_apparent({"x": 0, "y": 0, "z": 0}, star_pos)
        req = ObservationRequest(ra, dec, "imager", "clear", 300)
        result = self.telescope.observe("test", req)
        self.assertIn("headers", result)
        self.assertIn("data", result)
        self.assertEqual(result["data"]["type"], "image")
        names = [d.get("name") for d in result["data"]["detections"]]
        self.assertIn("Kael's Star", names)

    def test_radio_observation_finds_pulsar(self):
        pulsar_pos = {"x": 0.015, "y": -0.012, "z": -0.008}
        ra, dec, _ = position_to_apparent({"x": 0, "y": 0, "z": 0}, pulsar_pos)
        req = ObservationRequest(ra, dec, "radio_receiver", None, 300)
        result = self.telescope.observe("test", req)
        self.assertEqual(result["data"]["type"], "radio_map")
        names = [d.get("name") for d in result["data"]["detections"]]
        self.assertIn("Vorantis Pulsar", names)

    def test_spectrograph_acquires_target(self):
        star_pos = {"x": -0.004, "y": 0.009, "z": 0.001}
        ra, dec, _ = position_to_apparent({"x": 0, "y": 0, "z": 0}, star_pos)
        req = ObservationRequest(ra, dec, "spectrograph", "clear", 300)
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
        self.assertEqual(h["EXPTIME"], 60)
        self.assertEqual(h["FILTER"], "R_BAND")
        self.assertEqual(h["SCANPROF"], "survey")
        self.assertIn("DATE-OBS", h)
        self.assertIn("TELESCOP", h)

    def test_observation_returns_rewards(self):
        star_pos = {"x": -0.004, "y": 0.009, "z": 0.001}
        ra, dec, _ = position_to_apparent({"x": 0, "y": 0, "z": 0}, star_pos)
        req = ObservationRequest(ra, dec, "imager", "clear", 300)
        result = self.telescope.observe("test", req)
        self.assertIn("rewards", result["data"])
        self.assertIn("data", result["data"]["rewards"])

    def test_observation_returns_detection_ids(self):
        star_pos = {"x": -0.004, "y": 0.009, "z": 0.001}
        ra, dec, _ = position_to_apparent({"x": 0, "y": 0, "z": 0}, star_pos)
        req = ObservationRequest(ra, dec, "imager", "clear", 300)
        result = self.telescope.observe("test", req)
        for det in result["data"]["detections"]:
            self.assertIn("detection_id", det)
            self.assertTrue(det["detection_id"].startswith("det-"))

    def test_player_detection_optical(self):
        self.sky.players["other"] = PlayerSource(
            session_id="other",
            position_au={"x": 0.001, "y": 0.0, "z": 0.0},
            optical_glint=10.0,  # bright enough to detect
            last_tick=time.time(),
        )
        ra, dec, _ = position_to_apparent(
            {"x": 0, "y": 0, "z": 0}, {"x": 0.001, "y": 0.0, "z": 0.0})
        req = ObservationRequest(ra, dec, "imager", "clear", 300)
        result = self.telescope.observe("test", req)
        has_no_catalogue = any(
            len(d.get("catalogue_matches", [])) == 0
            for d in result["data"]["detections"]
        )
        self.assertTrue(has_no_catalogue)

    def test_player_detection_radio(self):
        self.sky.players["other"] = PlayerSource(
            session_id="other",
            position_au={"x": 0.001, "y": 0.0, "z": 0.0},
            radio_emissions=500.0,
            last_tick=time.time(),
        )
        ra, dec, _ = position_to_apparent(
            {"x": 0, "y": 0, "z": 0}, {"x": 0.001, "y": 0.0, "z": 0.0})
        req = ObservationRequest(ra, dec, "radio_receiver", None, 300)
        result = self.telescope.observe("test", req)
        has_no_catalogue = any(
            len(d.get("catalogue_matches", [])) == 0
            for d in result["data"]["detections"]
        )
        self.assertTrue(has_no_catalogue)

    def test_broadcast_increases_detectability(self):
        self.sky.players["other"] = PlayerSource(
            session_id="other",
            position_au={"x": 0.001, "y": 0.0, "z": 0.0},
            radio_emissions=5.0,
            broadcast_power=5.0,
            last_tick=time.time(),
        )
        ra, dec, _ = position_to_apparent(
            {"x": 0, "y": 0, "z": 0}, {"x": 0.001, "y": 0.0, "z": 0.0})
        req = ObservationRequest(ra, dec, "radio_receiver", None, 60)
        result = self.telescope.observe("test", req)
        # Broadcasting player should show up with no catalogue match
        player_dets = [
            d for d in result["data"]["detections"]
            if len(d.get("catalogue_matches", [])) == 0
        ]
        self.assertTrue(len(player_dets) > 0)

    def test_scan_profile_affects_snr(self):
        star_pos = {"x": -0.004, "y": 0.009, "z": 0.001}
        ra, dec, _ = position_to_apparent({"x": 0, "y": 0, "z": 0}, star_pos)

        req_survey = ObservationRequest(ra, dec, "imager", "clear", 60,
                                        scan_profile="survey")
        req_boosted = ObservationRequest(ra, dec, "imager", "clear", 60,
                                         scan_profile="boosted")
        r1 = self.telescope.observe("test", req_survey)
        r2 = self.telescope.observe("test", req_boosted)

        # Find Kael's Star in both
        def find_star(data):
            for d in data["data"]["detections"]:
                if d.get("name") == "Kael's Star":
                    return d["snr"]
            return 0

        snr_survey = find_star(r1)
        snr_boosted = find_star(r2)
        self.assertGreater(snr_boosted, snr_survey)


class TestSessionStore(unittest.TestCase):

    def setUp(self):
        self.store = SessionStore()

    def test_create_session(self):
        session = self.store.create_session()
        self.assertIsNotNone(session.session_id)
        self.assertIn(session.session_id, self.store.sky.players)

    def test_session_has_economy(self):
        session = self.store.create_session()
        d = self.store.session_to_dict(session)
        self.assertIn("economy", d)
        self.assertEqual(d["economy"]["credits"], 0)
        self.assertEqual(d["economy"]["unbanked_data"], 0)
        self.assertEqual(d["economy"]["intel"], 0)

    def test_session_has_physical_state(self):
        session = self.store.create_session()
        d = self.store.session_to_dict(session)
        self.assertIn("physical_state", d)
        self.assertIn("power_draw", d["physical_state"])
        self.assertIn("stored_heat", d["physical_state"])
        self.assertIn("radiator_mode", d["physical_state"])

    def test_session_has_signatures(self):
        session = self.store.create_session()
        d = self.store.session_to_dict(session)
        self.assertIn("signatures", d)

    def test_session_has_loadout(self):
        session = self.store.create_session()
        d = self.store.session_to_dict(session)
        self.assertIn("loadout", d)
        self.assertEqual(d["loadout"]["passive_modules"], [])
        self.assertEqual(d["loadout"]["active_modules"], [])

    def test_session_has_position(self):
        session = self.store.create_session()
        d = self.store.session_to_dict(session)
        self.assertIn("position_au", d["telescope"])

    def test_submit_and_check_observation(self):
        session = self.store.create_session()
        # Point at some sky location
        req = ObservationRequest(0, 0, "imager", "clear", 60)
        job = self.store.submit_observation(session.session_id, req)
        self.assertEqual(job.status.value, "processing")

        # Force ready by backdating start time
        job.started_at = time.time() - 100
        checked = self.store.check_job(session.session_id, job.job_id)
        self.assertEqual(checked.status.value, "completed")
        self.assertIsNotNone(checked.result)

    def test_observation_generates_heat(self):
        session = self.store.create_session()
        initial_heat = session.player_source.stored_heat
        req = ObservationRequest(0, 0, "imager", "clear", 300)
        self.store.submit_observation(session.session_id, req)
        self.assertGreater(session.player_source.stored_heat, initial_heat)

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

    def test_radiator_mode(self):
        session = self.store.create_session()
        result = self.store.set_radiator_mode(session.session_id, "venting")
        self.assertEqual(result["radiator_mode"], "venting")
        self.assertEqual(
            session.player_source.radiator_mode, "venting")

    def test_radiator_invalid_mode(self):
        session = self.store.create_session()
        with self.assertRaises(ValueError):
            self.store.set_radiator_mode(session.session_id, "turbo")

    def test_science_uplink(self):
        session = self.store.create_session()
        session.unbanked_data = 50
        result = self.store.uplink(session.session_id, {"report_type": "science"})
        self.assertEqual(result["status"], "accepted")
        self.assertEqual(result["banked_credits"], 50)
        self.assertEqual(session.credits, 50)
        self.assertEqual(session.unbanked_data, 0)

    def test_uplink_cooldown(self):
        session = self.store.create_session()
        session.unbanked_data = 10
        self.store.uplink(session.session_id, {"report_type": "science"})
        # Second uplink should fail due to cooldown
        with self.assertRaises(ValueError):
            self.store.uplink(session.session_id, {"report_type": "science"})

    def test_uplink_generates_heat(self):
        session = self.store.create_session()
        session.unbanked_data = 10
        initial_heat = session.player_source.stored_heat
        self.store.uplink(session.session_id, {"report_type": "science"})
        self.assertGreater(session.player_source.stored_heat, initial_heat)

    def test_hunt_uplink_miss(self):
        session = self.store.create_session()
        result = self.store.uplink(session.session_id, {
            "report_type": "hunt",
            "classification_guess": "artificial",
            "predicted_position_au": {"x": 99.0, "y": 99.0, "z": 99.0},
        })
        # No target nearby, should be a miss
        self.assertEqual(result["score"]["effective_hit_score"], 0.0)
        self.assertEqual(result["rewards"]["intel"], 0)

    def test_loadout(self):
        session = self.store.create_session()
        result = self.store.set_loadout(
            session.session_id,
            passive=["cold_baffles"],
            active=[],
        )
        self.assertEqual(result["passive_modules"], ["cold_baffles"])

    def test_loadout_invalid_module(self):
        session = self.store.create_session()
        with self.assertRaises(ValueError):
            self.store.set_loadout(
                session.session_id,
                passive=["nonexistent"],
                active=[],
            )

    def test_jump_start(self):
        session = self.store.create_session()
        dest = {"x": 0.01, "y": 0.0, "z": 0.0}
        result = self.store.start_jump(session.session_id, dest, "standard")
        self.assertIn("job_id", result)
        self.assertEqual(result["status"], "charging")
        self.assertTrue(result["observations_allowed"])
        self.assertEqual(session.jump_state, "jump_charging")

    def test_jump_cannot_start_while_charging(self):
        session = self.store.create_session()
        dest = {"x": 0.01, "y": 0.0, "z": 0.0}
        self.store.start_jump(session.session_id, dest, "standard")
        with self.assertRaises(ValueError):
            self.store.start_jump(session.session_id, dest, "standard")

    def test_jump_abort(self):
        session = self.store.create_session()
        dest = {"x": 0.01, "y": 0.0, "z": 0.0}
        result = self.store.start_jump(session.session_id, dest, "standard")
        job_id = result["job_id"]
        abort_result = self.store.abort_jump(session.session_id, job_id)
        self.assertEqual(abort_result["status"], "aborted")
        self.assertEqual(session.jump_state, "idle")

    def test_regions_endpoint(self):
        # Verify region data is accessible
        self.assertGreater(len(REGIONS), 0)
        for r in REGIONS:
            self.assertIsNotNone(r.id)
            self.assertIsNotNone(r.name)
            self.assertIn("x", r.center_au)


class TestNewFeatures(unittest.TestCase):
    """Tests for gap fixes: science scoring, active modules, tracks, jam, heat penalty."""

    def setUp(self):
        self.store = SessionStore()

    def test_observation_has_signature_report(self):
        session = self.store.create_session()
        req = ObservationRequest(0, 0, "imager", "clear", 60)
        job = self.store.submit_observation(session.session_id, req)
        job.started_at = time.time() - 100
        checked = self.store.check_job(session.session_id, job.job_id)
        self.assertIn("signature_report", checked.result["data"])
        sig = checked.result["data"]["signature_report"]
        self.assertIn("heat_generated", sig)
        self.assertIn("power_draw", sig)

    def test_science_uplink_with_question(self):
        session = self.store.create_session()
        # Greystone asteroid has hidden_state spin_period_sec=14310
        result = self.store.uplink(session.session_id, {
            "report_type": "science",
            "target_id": "ast-101",
            "question_id": "spin_period_sec",
            "estimate": 14310,  # exact match
        })
        self.assertEqual(result["status"], "accepted")
        self.assertIn("score", result)
        self.assertGreater(result["score"]["accuracy"], 0.9)
        self.assertGreater(result["rewards"]["data"], 0)

    def test_science_uplink_diminishing_returns(self):
        session = self.store.create_session()
        r1 = self.store.uplink(session.session_id, {
            "report_type": "science",
            "target_id": "ast-101",
            "question_id": "spin_period_sec",
            "estimate": 14310,
        })
        session.science_uplink_ready_at = 0  # bypass cooldown
        r2 = self.store.uplink(session.session_id, {
            "report_type": "science",
            "target_id": "ast-101",
            "question_id": "spin_period_sec",
            "estimate": 14310,
        })
        # Second report on same target/question should have lower novelty
        self.assertLess(r2["score"]["novelty"], r1["score"]["novelty"])

    def test_science_uplink_bad_estimate(self):
        session = self.store.create_session()
        result = self.store.uplink(session.session_id, {
            "report_type": "science",
            "target_id": "ast-101",
            "question_id": "spin_period_sec",
            "estimate": 999999,  # way off
        })
        self.assertLess(result["score"]["accuracy"], 0.1)

    def test_scored_science_pays_unbanked_not_credits(self):
        session = self.store.create_session()
        session.unbanked_data = 0
        session.credits = 0
        self.store.uplink(session.session_id, {
            "report_type": "science",
            "target_id": "ast-101",
            "question_id": "spin_period_sec",
            "estimate": 14310,
        })
        # Reward lands in unbanked_data, not credits
        self.assertGreater(session.unbanked_data, 0)
        self.assertEqual(session.credits, 0)

    def test_repeat_observation_diminishing_data(self):
        session = self.store.create_session()
        star_pos = {"x": -0.004, "y": 0.009, "z": 0.001}
        ra, dec, _ = position_to_apparent(
            session.player_source.position_au, star_pos)
        req = ObservationRequest(ra, dec, "imager", "clear", 300)

        # First observation
        job1 = self.store.submit_observation(session.session_id, req)
        job1.started_at = time.time() - 100
        self.store.check_job(session.session_id, job1.job_id)
        data_after_first = session.unbanked_data

        # Second identical observation
        job2 = self.store.submit_observation(session.session_id, req)
        job2.started_at = time.time() - 100
        data_before_second = session.unbanked_data
        self.store.check_job(session.session_id, job2.job_id)
        data_from_second = session.unbanked_data - data_before_second

        # Second should pay less than first
        self.assertLessEqual(data_from_second, data_after_first)

    def test_track_file_has_observer_position(self):
        session = self.store.create_session()
        self.store.sky.players["other"] = PlayerSource(
            session_id="other",
            position_au={"x": session.player_source.position_au["x"] + 0.001,
                         "y": session.player_source.position_au["y"],
                         "z": session.player_source.position_au["z"]},
            radio_emissions=500.0,
            last_tick=time.time(),
        )
        ra, dec, _ = position_to_apparent(
            session.player_source.position_au,
            self.store.sky.players["other"].position_au)
        req = ObservationRequest(ra, dec, "radio_receiver", None, 300)
        job = self.store.submit_observation(session.session_id, req)
        job.started_at = time.time() - 100
        self.store.check_job(session.session_id, job.job_id)
        tracks = self.store.track_manager.get_session_tracks(session.session_id)
        self.assertGreater(len(tracks), 0)
        t = self.store.track_manager.track_to_dict(tracks[0])
        ev = t["evidence"][0]
        self.assertIn("observer_position_au", ev)
        self.assertIn("x", ev["observer_position_au"])
        self.assertIn("observation_epoch", ev)

    def test_cold_baffles_reduce_glint(self):
        session = self.store.create_session()
        self.store.set_loadout(session.session_id,
                               passive=["cold_baffles"], active=[])
        self.store.get_session(session.session_id)  # trigger tick
        self.assertLess(session.player_source.optical_glint, 0.1)

    def test_signal_scrubber_reduces_radio(self):
        session = self.store.create_session()
        baseline = session.player_source.radio_emissions
        self.store.set_loadout(session.session_id,
                               passive=["signal_scrubber"], active=[])
        self.store.get_session(session.session_id)
        self.assertLess(session.player_source.radio_emissions, baseline)

    def test_heat_penalty_degrades_snr(self):
        sky = Sky(seed=42)
        telescope = Telescope(sky, rng_seed=42)
        sky.players["test"] = PlayerSource(
            session_id="test",
            position_au={"x": 0.0, "y": 0.0, "z": 0.0},
            stored_heat=0.0,
            last_tick=time.time(),
        )
        # Get baseline SNR
        star_pos = {"x": -0.004, "y": 0.009, "z": 0.001}
        ra, dec, _ = position_to_apparent({"x": 0, "y": 0, "z": 0}, star_pos)
        req = ObservationRequest(ra, dec, "imager", "clear", 300)
        r1 = telescope.observe("test", req)
        snr1 = 0
        for d in r1["data"]["detections"]:
            if d.get("name") == "Kael's Star":
                snr1 = d["snr"]

        # Now with high heat
        sky.players["test"].stored_heat = 1.5
        r2 = telescope.observe("test", req)
        snr2 = 0
        for d in r2["data"]["detections"]:
            if d.get("name") == "Kael's Star":
                snr2 = d["snr"]

        self.assertGreater(snr1, snr2)

    def test_track_files_auto_created(self):
        session = self.store.create_session()
        # Place another player nearby
        self.store.sky.players["other"] = PlayerSource(
            session_id="other",
            position_au={"x": session.player_source.position_au["x"] + 0.001,
                         "y": session.player_source.position_au["y"],
                         "z": session.player_source.position_au["z"]},
            radio_emissions=500.0,
            last_tick=time.time(),
        )
        # Observe toward them
        ra, dec, _ = position_to_apparent(
            session.player_source.position_au,
            self.store.sky.players["other"].position_au)
        req = ObservationRequest(ra, dec, "radio_receiver", None, 300)
        job = self.store.submit_observation(session.session_id, req)
        job.started_at = time.time() - 100
        self.store.check_job(session.session_id, job.job_id)
        # Track files should now have entries
        tracks = self.store.track_manager.get_session_tracks(session.session_id)
        self.assertGreater(len(tracks), 0)

    def test_session_has_recalibration_remaining(self):
        session = self.store.create_session()
        d = self.store.session_to_dict(session)
        self.assertIn("recalibration_remaining_sec", d)

    def test_jam_affects_targets(self):
        session = self.store.create_session()
        # Equip jammer
        self.store.set_loadout(session.session_id, passive=[], active=["directional_jammer"])
        # Create a target session very close
        target_session = self.store.create_session()
        target_session.player_source.position_au = {
            "x": session.player_source.position_au["x"] + 0.0001,
            "y": session.player_source.position_au["y"],
            "z": session.player_source.position_au["z"],
        }
        self.store.sky.players[target_session.session_id].position_au = (
            target_session.player_source.position_au)

        # Target should NOT have their radio_emissions changed (that was the bug)
        initial_radio = target_session.player_source.radio_emissions
        ra, dec, _ = position_to_apparent(
            session.player_source.position_au,
            target_session.player_source.position_au)
        result = self.store.jam(session.session_id, ra, dec)
        self.assertGreater(result["affected_targets"], 0)
        # Target radio_emissions unchanged — jam doesn't make target louder
        self.assertEqual(target_session.player_source.radio_emissions, initial_radio)
        # But target session has jam state
        self.assertGreater(target_session.radio_jam_strength, 0)


class TestPatchGroup1(unittest.TestCase):
    """Tests for followup items 1-4."""

    def setUp(self):
        self.store = SessionStore()

    # -- Item 1: hunt reports are guess-only --

    def test_hunt_without_evidence(self):
        session = self.store.create_session()
        result = self.store.uplink(session.session_id, {
            "report_type": "hunt",
            "classification_guess": "artificial",
            "predicted_position_au": {"x": 0.0, "y": 0.0, "z": 0.0},
        })
        # Should succeed without evidence_job_ids
        self.assertEqual(result["status"], "accepted")

    def test_hunt_only_needs_guess_and_position(self):
        session = self.store.create_session()
        # Minimal valid hunt payload: just classification + position
        r = self.store.uplink(session.session_id, {
            "report_type": "hunt",
            "classification_guess": "artificial",
            "predicted_position_au": {"x": 0.0, "y": 0.0, "z": 0.0},
        })
        self.assertEqual(r["status"], "accepted")
        self.assertIn("score", r)

    # -- Item 2: charged-hold timing --

    def test_charge_completes_without_poll(self):
        session = self.store.create_session()
        dest = {"x": session.player_source.position_au["x"] + 0.0001,
                "y": 0.0, "z": 0.0}
        result = self.store.start_jump(session.session_id, dest, "standard")
        job_id = result["job_id"]
        job = self.store.job_queue.get_jump_job(job_id)

        # Backdate start so charge would have completed 5s ago
        job.started_at = time.time() - job.charge_duration_sec - 5

        # Don't call check_jump — just tick via get_session
        s = self.store.get_session(session.session_id)
        self.assertEqual(s.jump_state, "jump_charged")
        # charged_at should be at real completion time, not poll time
        self.assertAlmostEqual(
            job.charged_at,
            job.started_at + job.charge_duration_sec,
            places=1)

    def test_auto_abort_uses_real_completion_time(self):
        session = self.store.create_session()
        dest = {"x": session.player_source.position_au["x"] + 0.0001,
                "y": 0.0, "z": 0.0}
        result = self.store.start_jump(session.session_id, dest, "standard")
        job_id = result["job_id"]
        job = self.store.job_queue.get_jump_job(job_id)

        # Backdate so charge completed 40s ago (past MAX_CHARGED_HOLD_SEC=30)
        job.started_at = time.time() - job.charge_duration_sec - 40

        s = self.store.get_session(session.session_id)
        # Should be auto-aborted, not still charged
        self.assertEqual(s.jump_state, "idle")

    # -- Item 3: jamming degrades target radio, not emissions --

    def test_jammed_target_higher_radio_noise(self):
        """A jammed observer sees worse radio observations."""
        session = self.store.create_session()
        # Set jam state directly
        session.radio_jam_strength = 5.0
        session.radio_jam_until = time.time() + 60

        # Observe with radio
        req = ObservationRequest(0, 0, "radio_receiver", None, 300)
        job = self.store.submit_observation(session.session_id, req)
        job.started_at = time.time() - 100
        checked = self.store.check_job(session.session_id, job.job_id)
        jammed_noise = checked.result["data"]["noise_floor_mJy"]

        # Compare with unjammed session
        session2 = self.store.create_session()
        req2 = ObservationRequest(0, 0, "radio_receiver", None, 300)
        job2 = self.store.submit_observation(session2.session_id, req2)
        job2.started_at = time.time() - 100
        checked2 = self.store.check_job(session2.session_id, job2.job_id)
        clean_noise = checked2.result["data"]["noise_floor_mJy"]

        self.assertGreater(jammed_noise, clean_noise)

    # -- Item 4: broadcast_power vs radio burst --

    def test_uplink_creates_burst_not_permanent_broadcast(self):
        session = self.store.create_session()
        session.unbanked_data = 10
        initial_broadcast = session.player_source.broadcast_power

        self.store.uplink(session.session_id, {"report_type": "science"})

        # broadcast_power should NOT have changed
        self.assertEqual(session.player_source.broadcast_power, initial_broadcast)
        # radio_burst_power should be set
        self.assertGreater(session.player_source.radio_burst_power, 0)
        self.assertGreater(session.player_source.radio_burst_until, 0)

    def test_burst_decays_after_expiry(self):
        session = self.store.create_session()
        p = session.player_source
        p.radio_burst_power = 5.0
        p.radio_burst_until = time.time() - 1  # already expired

        self.sky = self.store.sky
        self.store.sky.tick_player(session.session_id, time.time())
        self.assertEqual(p.radio_burst_power, 0.0)

    def test_optical_not_affected_by_radio_broadcast(self):
        """Optical brightness should not change based on broadcast_power."""
        sky = Sky(seed=42)
        telescope = Telescope(sky, rng_seed=42)
        sky.players["test"] = PlayerSource(
            session_id="test",
            position_au={"x": 0.0, "y": 0.0, "z": 0.0},
            last_tick=time.time(),
        )
        # Place a target
        sky.players["other"] = PlayerSource(
            session_id="other",
            position_au={"x": 0.001, "y": 0.0, "z": 0.0},
            optical_glint=10.0,
            broadcast_power=0.0,
            last_tick=time.time(),
        )
        ra, dec, _ = position_to_apparent(
            {"x": 0, "y": 0, "z": 0}, {"x": 0.001, "y": 0.0, "z": 0.0})
        req = ObservationRequest(ra, dec, "imager", "clear", 300)
        r1 = telescope.observe("test", req)

        # Now give the target high broadcast_power
        sky.players["other"].broadcast_power = 10.0
        r2 = telescope.observe("test", req)

        # Find the player detection in both
        def find_uncat(data):
            for d in data["data"]["detections"]:
                if len(d.get("catalogue_matches", [])) == 0:
                    return d.get("flux", {}).get("optical_mag", 30)
            return 30

        mag1 = find_uncat(r1)
        mag2 = find_uncat(r2)
        # Optical brightness should be the same — broadcast is radio-only
        self.assertAlmostEqual(mag1, mag2, places=1)


if __name__ == "__main__":
    unittest.main()
