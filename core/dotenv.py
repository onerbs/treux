def _find(name: str, root) -> str:
	if (parent := root.parent) == root:
		return ''

	from os import listdir
	return _find(name, parent) \
		if root.is_file() or name not in listdir(root) \
		else str(root / name)


def _parse(plain: str) -> dict:
	env = {}
	for line in plain.splitlines():
		if '=' in line:
			k, v = line.split('=', 1)
			env.update({k: v})
	return env


def _source(file_path: str, override: bool) -> None:
	if not file_path:
		return

	from os import environ
	with open(file_path) as file:
		for k, v in _parse(file.read()).items():
			if override:
				environ[k] = v
			else:
				environ.setdefault(k, v)


def source(secondary=None, override=False) -> None:
	"""Source the dotenv file.

	A secondary dotenv file is, for example `.env.secondary`

	By default, the already-defined values will take precedence over those
	defined in the dotenv file. To change this behavior, pass the `override`
	parameter set to `True`.

	:param secondary: The secondary dotenv file name.
	:param override: Whether or not to override values.
	"""
	from pathlib import Path
	__this__ = Path(__file__)

	_source(_find('.env', __this__), override)

	if secondary is not None:
		_source(_find(f'.{secondary.lower()}', __this__), True)
