"""Estimate storage used by a tree of files and folders."""

from __future__ import annotations

import unittest


class Entry:
	"""Base class for a named filesystem entry."""

	def __init__(self: Entry, name: str, parent: Entry | None = None) -> None:
		"""Initialize an entry with its name and optional parent."""
		self.name: str = name
		self._parent: Entry | None = parent

	def parent(self: Entry) -> Entry | None:
		"""Return this entry's parent, or None when it is a root entry."""
		return self._parent

	def size(self: Entry) -> int:
		"""Return the entry's size in bytes."""
		raise NotImplementedError("Entry subclasses must implement size().")

	def absolute_path(self: Entry) -> list[Entry]:
		"""Return entries from this entry up to and including the root."""
		if self._parent is None:
			return [self]
		return [self, *self._parent.absolute_path()]


class File(Entry):
	"""A file with a fixed, nonnegative storage size."""

	def __init__(self: File, name: str, bytes_used: int, parent: Entry | None = None) -> None:
		"""Initialize a file and reject negative storage sizes."""
		super().__init__(name, parent)
		if bytes_used < 0:
			raise ValueError("bytes_used must be nonnegative.")
		self.bytes_used: int = bytes_used

	def size(self: File) -> int:
		"""Return the number of bytes used by this file."""
		return self.bytes_used


class Folder(Entry):
	"""A folder containing files and other folders."""

	def __init__(self: Folder, name: str, parent: Entry | None = None) -> None:
		"""Initialize an empty folder."""
		super().__init__(name, parent)
		self._children: list[Entry] = []

	def add(self: Folder, entry: Entry) -> None:
		"""Add an entry as a child and set its parent to this folder."""
		entry._parent = self
		self._children.append(entry)

	def size(self: Folder) -> int:
		"""Return the combined size of all files in this folder tree."""
		return sum(entry.size() for entry in self._children)

	def children(self: Folder) -> tuple[Entry, ...]:
		"""Return this folder's direct children as an immutable tuple."""
		return tuple(self._children)


def find_large_files(entry: Entry, minimum_size: int) -> list[File]:
	"""Find files at least minimum_size bytes below entry.

	If entry is a File, return that file when it meets the threshold;
	if entry is a Folder, search all of its descendants recursively.
	"""
	if isinstance(entry, File):
		return [entry] if entry.size() >= minimum_size else []
	if isinstance(entry, Folder):
		return [
			file
			for child in entry.children()
			for file in find_large_files(child, minimum_size)
		]
	return []


class EntryHierarchyTests(unittest.TestCase):
	"""Tests for recursive size, search, and absolute-path behavior."""

	def setUp(self: EntryHierarchyTests) -> None:
		"""Create a three-level nested tree for each test."""
		self.root = Folder("root")
		self.archive = Folder("archive")
		self.department = Folder("department")
		self.lab = Folder("lab")
		self.root.add(self.archive)
		self.archive.add(self.department)
		self.department.add(self.lab)
		self.root.add(File("readme.txt", 300))
		self.archive.add(File("dataset.csv", 1800))
		self.department.add(File("notes.txt", 900))
		self.lab.add(File("simulation.bin", 6400))
		self.lab.add(File("image.raw", 2100))

	def test_find_large_files_in_folder_at_two_thresholds(self: EntryHierarchyTests) -> None:
		"""Return all nested files meeting each requested threshold."""
		self.assertEqual(
			{file.name for file in find_large_files(self.root, 1000)},
			{"dataset.csv", "simulation.bin", "image.raw"},
		)
		self.assertEqual(
			{file.name for file in find_large_files(self.root, 2500)},
			{"simulation.bin"},
		)

	def test_find_large_files_when_entry_is_file(self: EntryHierarchyTests) -> None:
		"""Search a file entry itself, including threshold boundaries."""
		large_file = self.lab.children()[0]
		self.assertIsInstance(large_file, File)
		self.assertEqual(find_large_files(large_file, 6400), [large_file])
		self.assertEqual(find_large_files(large_file, 6401), [])

	def test_absolute_path_runs_from_entry_to_root(self: EntryHierarchyTests) -> None:
		"""Return the current entry followed by each ancestor."""
		simulation_file = self.lab.children()[0]
		self.assertEqual(
			[entry.name for entry in simulation_file.absolute_path()],
			["simulation.bin", "lab", "department", "archive", "root"],
		)

	def test_root_absolute_path_contains_only_root(self: EntryHierarchyTests) -> None:
		"""Return a one-entry path for a root folder."""
		self.assertEqual(self.root.absolute_path(), [self.root])


def build_example_hierarchy() -> Folder:
	"""Build and return a sample hierarchy with four folder levels."""
	root = Folder("university")
	archive = Folder("archive")
	department = Folder("physics")
	lab = Folder("research-lab")
	root.add(archive)
	archive.add(department)
	department.add(lab)
	root.add(File("catalog.txt", 300))
	archive.add(File("enrollment.csv", 1800))
	department.add(File("schedule.txt", 900))
	lab.add(File("simulation.bin", 6400))
	lab.add(File("image.raw", 2100))
	return root


def demonstrate() -> None:
	"""Print recursive size, searches at two thresholds, and one path."""
	root = build_example_hierarchy()
	print(f"Total storage: {root.size()} bytes")
	for minimum_size in (1000, 2500):
		names = [file.name for file in find_large_files(root, minimum_size)]
		print(f"Files at least {minimum_size} bytes: {names}")
	example_file = find_large_files(root, 6400)[0]
	print("Absolute path:", [entry.name for entry in example_file.absolute_path()])


if __name__ == "__main__":
	unittest.main(exit=False)
	demonstrate()
