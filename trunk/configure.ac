AC_INIT(persephone,0.0,edA-qa@disemia.com)

AC_PATH_PROG([JAVA],[java])

AC_PATH_PROG([PYTHON],[python])
AX_PROG_PYTHON_VERSION([2.5],
	[],
	[AC_MSG_ERROR([The generator requires Python 2.5 or greater])])

dnl Perhaps the run-time dependencies should be a separate script?
AC_PATH_PROG([PHP],[php])
AX_PROG_PHP_VERSION([5.2],[],[AC_MSG_ERROR([Requires PHP 5.2 or higher])])

AC_PATH_PROG([PEAR],[pear])
AX_PEAR_MODULE([MDB2],[2.0],[],[AC_MSG_WARN([MDB2 is not available])])
AX_PEAR_MODULE([MDB2_Driver_mysqli],[1.0],[],[AC_MSG_WARN([MDB2 MySQLI is not available])])
AX_PEAR_MODULE([HTML_QuickForm],[3.2],[],[AC_MSG_WARN([HTML_QuickForm is not available, Forms will not work])])
AX_PEAR_MODULE([Date],[1.4],[],[AC_MSG_ERROR([Requires pear module Date: pear install Date])])

AC_OUTPUT