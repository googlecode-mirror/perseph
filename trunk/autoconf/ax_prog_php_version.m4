# Based on ax_prog_python_version.m4
AC_DEFUN([AX_PROG_PHP_VERSION],[
	AC_REQUIRE([AC_PROG_SED])
	AC_REQUIRE([AC_PROG_GREP])
	
	AS_IF([test -n "$PYTHON"],[
		ax_php_version="$1"
		AC_MSG_CHECKING([for php version])
		changequote(<<,>>)
		php_version=`$PHP --version | $GREP "^PHP " | $SED -e 's/^.* \([0-9]*\.[0-9]*\.[0-9]*\).*/\1/'`
		changequote([,])
		AC_MSG_RESULT($php_version)
	
		AC_SUBST([PHP_VERSION],[$php_version])
	
		AX_COMPARE_VERSION([$ax_php_version],[le],[$php_version],[
		:
				$2
		],[
		:
				$3
		])
	],[
		AC_MSG_WARN([could not find php])
	])
])
