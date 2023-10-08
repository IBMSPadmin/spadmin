# From here: https://stackoverflow.com/questions/12523586/python-format-size-application-converting-b-to-kb-mb-gb-tb

from typing import List, Union

import lib.globals as globals

class HumanBytes:
	METRIC_LABELS: List[ str ]       = [ "B", "kB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB" ]
	BINARY_LABELS: List[ str ]       = [ "B", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB" ]
	TIME_LABELS: List[ str ]         = [ "s", "m", "H", "d", "w", "Mo", "Y" ]
	TIME_UNIT: List[ str ]           = [ 1, 60, 60, 24, 7, 30, 12, 1 ]
	PRECISION_OFFSETS: List[ float ] = [ 0.5, 0.05, 0.005, 0.0005 ] # PREDEFINED FOR SPEED.
	PRECISION_FORMATS: List[ str ]   = [ "{}{:.0f} {}", "{}{:.1f} {}", "{}{:.2f} {}", "{}{:.3f} {}" ] # PREDEFINED FOR SPEED.

	#@staticmethod
	def format( num: Union[ int, float ], unit: str = "BINARY_LABELS", precision: int = 1 ) -> str:
		"""
		Human-readable formatting of bytes, using binary (powers of 1024)
		or metric (powers of 1000) representation.
		"""
		
		if globals.nohumanreadable == 'True':
			return str( num )

		assert isinstance( num, ( int, float ) ), "num must be an int or float"
		assert isinstance( precision, int ) and precision >= 0 and precision <= 3, "precision must be an int (range 0-3)"

		unit_labels = HumanBytes.BINARY_LABELS
		if unit == "BINARY_LABELS":
			unit_labels = HumanBytes.BINARY_LABELS
		elif unit == "METRIC_LABELS":
			unit_labels = HumanBytes.METRIC_LABELS
		elif unit == "TIME_LABELS":
			unit_labels = HumanBytes.TIME_LABELS

		last_label       = unit_labels[ -1 ]
		unit_step        = 1000 if unit_labels == HumanBytes.METRIC_LABELS else 1024
		unit_step_thresh = unit_step - HumanBytes.PRECISION_OFFSETS[ precision ]

		is_negative = num < 0
		if is_negative: # Faster than ternary assignment or always running abs().
			num = abs( num )

		if unit == "TIME_LABELS":
			i = 1;
			for unit in unit_labels:
				if num < HumanBytes.TIME_UNIT[i]:
					break
				if unit != last_label:
					num /= HumanBytes.TIME_UNIT[i]
					i += 1
			return HumanBytes.PRECISION_FORMATS[0].format("-" if is_negative else "", num, unit)

		for unit in unit_labels:
			if num < unit_step_thresh:
				# VERY IMPORTANT:
				# Only accepts the CURRENT unit if we're BELOW the threshold where
				# float rounding behavior would place us into the NEXT unit: F.ex.
				# when rounding a float to 1 decimal, any number ">= 1023.95" will
				# be rounded to "1024.0". Obviously we don't want ugly output such
				# as "1024.0 KiB", since the proper term for that is "1.0 MiB".
				break
			if unit != last_label:
				# We only shrink the number if we HAVEN'T reached the last unit.
				# NOTE: These looped divisions accumulate floating point rounding
				# errors, but each new division pushes the rounding errors further
				# and further down in the decimals, so it doesn't matter at all.
				num /= unit_step

		return HumanBytes.PRECISION_FORMATS[ precision ].format( "-" if is_negative else "", num, unit )