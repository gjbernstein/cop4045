import os
import sys
import tempfile
import unittest
from datetime import datetime

DATE_FORMAT = "%I:%M:%S %p %m/%d/%Y"


def read_observations(filename):
    observations = {}
    errors = []
    seen_dates = {}

    with open(filename, "r", encoding="utf-8") as infile:
        for line_number, raw_line in enumerate(infile, start=1):
            line = raw_line.strip()
            if not line:
                errors.append((line_number, "empty line"))
                continue

            parts = [part.strip() for part in line.split(",")]
            if len(parts) != 3:
                errors.append((line_number, "malformed line"))
                continue

            station, date_text, temperature_text = parts
            if not station:
                errors.append((line_number, "missing station"))
                continue
            if not date_text:
                errors.append((line_number, "missing date"))
                continue

            try:
                parsed_date = datetime.strptime(date_text, DATE_FORMAT)
            except ValueError:
                errors.append((line_number, "invalid date"))
                continue

            try:
                temperature = float(temperature_text)
            except ValueError:
                errors.append((line_number, "invalid temperature"))
                continue

            if not -100.0 <= temperature <= 150.0:
                errors.append((line_number, "temperature out of range"))
                continue

            station_dates = seen_dates.setdefault(station, set())
            if parsed_date in station_dates:
                errors.append((line_number, "duplicate station/date combination"))
                continue

            station_dates.add(parsed_date)
            observations.setdefault(station, []).append((parsed_date, temperature))

    for station in observations:
        observations[station].sort(key=lambda item: item[0])

    return observations, errors


def station_statistics(observations):
    statistics = {}
    for station in sorted(observations):
        temperatures = [value for _, value in observations[station]]
        if not temperatures:
            continue
        statistics[station] = {
            "min": min(temperatures),
            "max": max(temperatures),
            "mean": sum(temperatures) / len(temperatures),
        }
    return statistics


def station_outliers(observations):
    statistics = station_statistics(observations)
    return {
        station: (observations[station][-1][0], observations[station][-1][1], statistics[station]["mean"])
        for station in observations
        if observations[station] and observations[station][-1][1] > statistics[station]["mean"]
    }


def write_statistics(filename, statistics):
    with open(filename, "w", encoding="utf-8") as outfile:
        outfile.write("station,min,max,mean\n")
        for station in sorted(statistics):
            station_stats = statistics[station]
            outfile.write(
                f"{station},{station_stats['min']:.1f},{station_stats['max']:.1f},{station_stats['mean']:.1f}\n"
            )


def main(argv=None):
    if argv is None:
        argv = sys.argv

    if len(argv) != 3:
        print("Usage: python p5_Bernstein_Gigi.py <input_file> <output_file>")
        return 1

    input_file, output_file = argv[1], argv[2]

    try:
        observations, errors = read_observations(input_file)
    except FileNotFoundError:
        print(f"Error: file '{input_file}' was not found.")
        return 1
    except OSError as exc:
        print(f"Error accessing '{input_file}': {exc}")
        return 1

    if errors:
        print("Errors encountered:")
        for line_number, message in errors:
            print(f"Line {line_number}: {message}")

    stats = station_statistics(observations)
    print("Station statistics:")
    for station in sorted(stats):
        station_stats = stats[station]
        print(
            f"{station}: min={station_stats['min']:.1f}, "
            f"max={station_stats['max']:.1f}, mean={station_stats['mean']:.1f}"
        )

    print("\nOutliers:")
    outliers = station_outliers(observations)
    if not outliers:
        print("None")
    else:
        for station in sorted(outliers):
            date_value, temperature, mean = outliers[station]
            print(f"{station}: {date_value} {temperature:.1f} > mean {mean:.1f}")

    try:
        write_statistics(output_file, stats)
    except OSError as exc:
        print(f"Error writing '{output_file}': {exc}")
        return 1

    return 0


class WeatherObservationTests(unittest.TestCase):
    def test_read_observations_multiple_stations_sorted(self):
        with tempfile.NamedTemporaryFile("w", delete=False, newline="") as handle:
            handle.write("Alpha,09:00:00 AM 04/20/2026,72.5\n")
            handle.write("Bravo,08:15:00 AM 04/19/2026,61.0\n")
            handle.write("Alpha,10:30:00 AM 04/21/2026,75.0\n")
            handle.write("Charlie,11:00:00 PM 12/31/2025,-5.5\n")
            name = handle.name

        try:
            observations, errors = read_observations(name)
            self.assertEqual(errors, [])
            self.assertEqual(list(observations), ["Alpha", "Bravo", "Charlie"])
            self.assertEqual(observations["Alpha"][0][0], datetime.strptime("09:00:00 AM 04/20/2026", DATE_FORMAT))
            self.assertEqual(observations["Alpha"][0][1], 72.5)
            self.assertEqual(observations["Alpha"][1][0], datetime.strptime("10:30:00 AM 04/21/2026", DATE_FORMAT))
        finally:
            os.unlink(name)

    def test_read_observations_negative_temperatures_allowed(self):
        with tempfile.NamedTemporaryFile("w", delete=False, newline="") as handle:
            handle.write("North,09:00:00 AM 04/20/2026,-8.0\n")
            name = handle.name

        try:
            observations, errors = read_observations(name)
            self.assertEqual(errors, [])
            self.assertEqual(observations["North"][0][1], -8.0)
        finally:
            os.unlink(name)

    def test_read_observations_duplicate_observation_rejected(self):
        with tempfile.NamedTemporaryFile("w", delete=False, newline="") as handle:
            handle.write("Alpha,09:00:00 AM 04/20/2026,70.0\n")
            handle.write("Alpha,09:00:00 AM 04/20/2026,70.0\n")
            name = handle.name

        try:
            observations, errors = read_observations(name)
            self.assertEqual(observations["Alpha"], [(datetime.strptime("09:00:00 AM 04/20/2026", DATE_FORMAT), 70.0)])
            self.assertTrue(any("duplicate" in message.lower() for _, message in errors))
        finally:
            os.unlink(name)

    def test_read_observations_invalid_temperature_range_rejected(self):
        with tempfile.NamedTemporaryFile("w", delete=False, newline="") as handle:
            handle.write("Alpha,09:00:00 AM 04/20/2026,200.0\n")
            handle.write("Bravo,09:00:00 AM 04/21/2026,-101.0\n")
            name = handle.name

        try:
            observations, errors = read_observations(name)
            self.assertEqual(observations, {})
            self.assertEqual(len(errors), 2)
        finally:
            os.unlink(name)

    def test_station_statistics_calculates_min_max_mean(self):
        observations = {
            "Alpha": [
                (datetime.strptime("09:00:00 AM 04/20/2026", DATE_FORMAT), 10.0),
                (datetime.strptime("09:00:00 AM 04/21/2026", DATE_FORMAT), 20.0),
                (datetime.strptime("09:00:00 AM 04/22/2026", DATE_FORMAT), 30.0),
            ],
            "Bravo": [
                (datetime.strptime("08:00:00 AM 04/20/2026", DATE_FORMAT), -5.0),
                (datetime.strptime("08:00:00 AM 04/21/2026", DATE_FORMAT), 5.0),
            ],
        }

        stats = station_statistics(observations)
        self.assertAlmostEqual(stats["Alpha"]["min"], 10.0)
        self.assertAlmostEqual(stats["Alpha"]["max"], 30.0)
        self.assertAlmostEqual(stats["Alpha"]["mean"], 20.0)
        self.assertAlmostEqual(stats["Bravo"]["min"], -5.0)
        self.assertAlmostEqual(stats["Bravo"]["max"], 5.0)
        self.assertAlmostEqual(stats["Bravo"]["mean"], 0.0)

    def test_station_outliers_uses_latest_temperature_and_mean(self):
        observations = {
            "Alpha": [
                (datetime.strptime("09:00:00 AM 04/20/2026", DATE_FORMAT), 10.0),
                (datetime.strptime("09:00:00 AM 04/21/2026", DATE_FORMAT), 30.0),
            ],
            "Bravo": [
                (datetime.strptime("08:00:00 AM 04/20/2026", DATE_FORMAT), 3.0),
                (datetime.strptime("08:00:00 AM 04/21/2026", DATE_FORMAT), 1.0),
            ],
        }

        outliers = station_outliers(observations)
        self.assertEqual(set(outliers), {"Alpha"})
        self.assertEqual(outliers["Alpha"][0], datetime.strptime("09:00:00 AM 04/21/2026", DATE_FORMAT))
        self.assertEqual(outliers["Alpha"][1], 30.0)
        self.assertAlmostEqual(outliers["Alpha"][2], 20.0)

    def test_write_statistics_formats_sorted_output(self):
        statistics = {
            "Bravo": {"min": 1.0, "max": 9.0, "mean": 5.0},
            "Alpha": {"min": 2.0, "max": 8.0, "mean": 5.0},
        }

        with tempfile.NamedTemporaryFile("w", delete=False, newline="") as handle:
            filename = handle.name

        try:
            write_statistics(filename, statistics)
            with open(filename, "r", encoding="utf-8") as infile:
                lines = infile.read().strip().splitlines()
            self.assertEqual(lines[0], "station,min,max,mean")
            self.assertEqual(lines[1], "Alpha,2.0,8.0,5.0")
            self.assertEqual(lines[2], "Bravo,1.0,9.0,5.0")
        finally:
            os.unlink(filename)

    def test_missing_file_raises_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            read_observations("this_file_does_not_exist.csv")


if __name__ == "__main__":
    raise SystemExit(main())
