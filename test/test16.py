import pypyrus_logbook as logbook


log = logbook.getlogger()

smth = 'Something'
log.info(smth)
log.blank()
log.info(smth)
log.blank(5)
log.info(smth)
