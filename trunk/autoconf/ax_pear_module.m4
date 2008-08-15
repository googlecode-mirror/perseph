# Based on ax_prog_python_version.m4
AC_DEFUN([AX_PEAR_MODULE],[
	AC_REQUIRE([AC_PROG_SED])
	AC_REQUIRE([AC_PROG_GREP])
	
	AS_IF([test -n "$PEAR"],[
		ax_pear_module="$1"
		ax_mod_version="$2"
		AC_MSG_CHECKING([for pear module $1/$2])
		changequote(<<,>>)
		pear_mod_version=`$PEAR list | $GREP "^$1 " | $SED -e 's/^.* \([0-9]*\.[0-9]*\.[0-9]*\).*/\1/'`
		changequote([,])
		AC_MSG_RESULT($pear_mod_version)
	
		AC_SUBST([PEAR_$1_VERSION],[$pear_mod_version])
	
		AX_COMPARE_VERSION([$ax_mod_version],[le],[$pear_mod_version],[
		:
				$3
		],[
		:
				$4
		])
	],[
		AC_MSG_WARN([could not find pear])
	])
])
