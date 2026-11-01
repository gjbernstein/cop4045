'''simple non-interactive text-file editing commands and demonstrations.'''

from __future__ import annotations

import os
import stat
import tempfile
from pathlib import Path

from testif import testif


def _validate_text(value: str, parameter_name: str) -> None:
	''' checks if text is string
	parameters:
	    value: the text to validate.
	    parameter_name: the name of the parameter for error messages
	return:
        none
	raise:
	    TypeError: if value is not a string.'''
	if not isinstance(value, str):
		raise TypeError(f"{parameter_name} must be a string")


def _write_atomically(filename: str, content: str) -> None:
	'''replaces filename with content, but leaves the original intact if theres a failure.
	parameters:
	    filename: the path to the file to replace
	    content: the new content to write to the file
	return:
	    none
	raise:
	    OSError: if there is an error writing to the temporary file or replacing the original file
	'''
	path = Path(filename)
	try:
		existing_mode = stat.S_IMODE(path.stat().st_mode)
	except FileNotFoundError:
		existing_mode = None

	with tempfile.TemporaryDirectory(dir=path.parent) as temp_directory:
		temporary_path = Path(temp_directory) / path.name
		temporary_path.write_text(content, encoding="utf-8")
		if existing_mode is not None:
			temporary_path.chmod(existing_mode)
		os.replace(temporary_path, path)


def ed_read(filename: str, from_pos: int = 0, to: int = -1) -> str:
	'''read and return the file text in the half-open interval [from_pos, to).

	preconditions: \
		- filename is a path string
		-  from_pos and to are integers
	    - from_pos is nonnegative
	    - to is -1 or nonnegative.
	postconditions: 
		- the file is unchanged and the requested text is returned
	    - if to is greater than the file length, raise IndexError
	    - File I/O errors propagate to the caller
	'''
	_validate_text(filename, "filename")
	if not isinstance(from_pos, int) or isinstance(from_pos, bool):
		raise TypeError("from_pos must be an integer")
	if not isinstance(to, int) or isinstance(to, bool):
		raise TypeError("to must be an integer")
	if from_pos < 0:
		raise ValueError("from_pos cannot be negative")
	if to < -1:
		raise ValueError("to must be -1 or nonnegative")

	content = Path(filename).read_text(encoding="utf-8")
	if to > len(content):
		raise IndexError(f"to ({to}) exceeds file length ({len(content)})")
	end = len(content) if to == -1 else to
	return content[from_pos:end]


def ed_find(filename: str, search_str: str) -> list[int]:
	'''return: 
	    - list of the non-overlapping start positions of search_str in the file.

	preconditions: 
	    - filename and search_str are strings.
	postconditions: 
	    - file is unchanged
		- an empty search string matches each character boundary, including after final character
	    - File I/O errors propagate to the caller
	'''
	_validate_text(filename, "filename")
	_validate_text(search_str, "search_str")
	content = Path(filename).read_text(encoding="utf-8")
	if search_str == "":
		return list(range(len(content) + 1))

	positions: list[int] = []
	start = 0
	while True:
		position = content.find(search_str, start)
		if position == -1:
			return positions
		positions.append(position)
		start = position + len(search_str)


def ed_replace(
	filename: str,
	search_str: str,
	replace_with: str,
	occurrence: int = -1,
) -> int:
	'''replace all or one indexed non-overlapping occurrence in a file.

	preconditions: 
	    - filename, search_str, and replace_with are strings
	    - occurrence is -1 (replace all) or a nonnegative integer
	postconditions: 
	    - returns the number of replacements
	    - An occurrence index beyond the matches returns 0 without changing the file
	    - The file is atomically replaced only after its new contents are ready
	    - File I/O errors propagate to the caller
	'''
	_validate_text(filename, "filename")
	_validate_text(search_str, "search_str")
	_validate_text(replace_with, "replace_with")
	if not isinstance(occurrence, int) or isinstance(occurrence, bool):
		raise TypeError("occurrence must be an integer")
	if occurrence < -1:
		raise ValueError("occurrence must be -1 or nonnegative")

	path = Path(filename)
	content = path.read_text(encoding="utf-8")
	positions = (
		list(range(len(content) + 1))
		if search_str == ""
		else ed_find(filename, search_str)
	)

	if occurrence == -1:
		if not positions:
			return 0
		updated_content = content.replace(search_str, replace_with)
		replacement_count = len(positions)
	elif occurrence >= len(positions):
		return 0
	else:
		position = positions[occurrence]
		updated_content = (
			content[:position]
			+ replace_with
			+ content[position + len(search_str):]
		)
		replacement_count = 1

	_write_atomically(filename, updated_content)
	return replacement_count


def ed_append(filename: str, string: str) -> int:
	'''Append string to filename, creating the file if it does not exist.

	preconditions: 
	    - filename and string are strings
	postconditions: 
	    - returns the number of characters appended
	    - File I/O errors propagate to the caller
	    - the target is replaced only after the updated contents have been written successfully
	'''
	_validate_text(filename, "filename")
	_validate_text(string, "string")
	path = Path(filename)
	try:
		original_content = path.read_text(encoding="utf-8")
	except FileNotFoundError:
		original_content = ""
	_write_atomically(filename, original_content + string)
	return len(string)


def test_ed_find() -> bool:
	'''test ed_find's positions, missing matches, and empty-string behavior'''
	with tempfile.TemporaryDirectory() as temp_directory:
		filename = str(Path(temp_directory) / "find_test.txt")
		ed_append(filename, "abc abc ab")
		positions_match = ed_find(filename, "abc") == [0, 4]
		no_match = ed_find(filename, "xyz") == []
		empty_match = ed_find(filename, "") == list(range(11))
		return all((
			testif(positions_match, "ed_find positions", "found both matches", "wrong positions"),
			testif(no_match, "ed_find missing text", "returned no matches", "unexpected match"),
			testif(empty_match, "ed_find empty string", "found text boundaries", "wrong boundaries"),
		))


def test_ed_replace() -> bool:
	'''test ed_replace's all, indexed, absent-index, and empty-string cases'''
	with tempfile.TemporaryDirectory() as temp_directory:
		filename = str(Path(temp_directory) / "replace_test.txt")
		ed_append(filename, "one two one")
		replaced_all = ed_replace(filename, "one", "1") == 2
		all_content_correct = ed_read(filename) == "1 two 1"
		replaced_one = ed_replace(filename, "1", "first", 1) == 1
		one_content_correct = ed_read(filename) == "1 two first"
		beyond_matches = ed_replace(filename, "1", "unused", 2) == 0
		unchanged_on_missing = ed_read(filename) == "1 two first"
		empty_replaced = ed_replace(filename, "", "|", 0) == 1
		empty_content_correct = ed_read(filename) == "|1 two first"
		return all((
			testif(replaced_all and all_content_correct, "ed_replace all", "replaced both matches", "all replacement failed"),
			testif(replaced_one and one_content_correct, "ed_replace occurrence", "replaced indexed match", "indexed replacement failed"),
			testif(beyond_matches and unchanged_on_missing, "ed_replace missing occurrence", "left file unchanged", "changed file unexpectedly"),
			testif(empty_replaced and empty_content_correct, "ed_replace empty string", "replaced at selected boundary", "empty search failed"),
		))


def main() -> None:
	'''run unit tests and demonstrate each editing command on a temporary file'''
	test_ed_find()
	test_ed_replace()

	with tempfile.TemporaryDirectory() as temp_directory:
		filename = str(Path(temp_directory) / "editor_demo.txt")
		appended = ed_append(filename, "0123456789")
		ed_append(filename, "0123456789")
		print(f"ed_append wrote {appended} characters")
		print(f"ed_read(3, 9): {ed_read(filename, 3, 9)}")
		print(f"ed_read(3): {ed_read(filename, 3)}")
		print(f"ed_find('345'): {ed_find(filename, '345')}")
		print(f"ed_find('356'): {ed_find(filename, '356')}")
		replacements = ed_replace(filename, "345", "ABCDE", 1)
		print(f"ed_replace occurrence 1 replaced {replacements} match")
		print(f"Final file contents: {ed_read(filename)}")
		print("name: Gigi Bernstein")
		print("Z number: Z23652485")


if __name__ == "__main__":
	main()
