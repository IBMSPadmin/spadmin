REPORTMDFILE="spreport.md"

./spadmin.py -a " \
	print # Simple SP report | noheader | file $REPORTMDFILE; \
  print ## Current sessions | noheader | fileappend $REPORTMDFILE; \
  sh sess | htmlout | fileappend $REPORTMDFILE; \
  
  print ## Current actew | noheader | fileappend $REPORTMDFILE; \
  print Here are the errors and warnings from the last 3 hours: | noheader | fileappend $REPORTMDFILE; \
  print <pre> | noheader | fileappend $REPORTMDFILE; \
  actew | nocolor | fileappend $REPORTMDFILE; \
  print </pre> | noheader | fileappend $REPORTMDFILE; \
  
  print ## Current stgps | noheader | fileappend $REPORTMDFILE; \
  print Here are the stgps: | noheader | fileappend $REPORTMDFILE; \
  print <pre> | noheader | fileappend $REPORTMDFILE; \
  sh stgp | nocolor | fileappend $REPORTMDFILE; \
  print </pre> | noheader | fileappend $REPORTMDFILE; \
  
  print ## Current copygs | noheader | fileappend $REPORTMDFILE; \
  print Here are the copygs: | noheader | fileappend $REPORTMDFILE; \
  print <pre> | noheader | fileappend $REPORTMDFILE; \
  sh copyg | nocolor | fileappend $REPORTMDFILE; \
  print </pre> | noheader | fileappend $REPORTMDFILE; \
  
  print ## Current events | noheader | fileappend $REPORTMDFILE; \
  sh events | htmlout | fileappend $REPORTMDFILE; \

  print ## Current adminevents | noheader | fileappend $REPORTMDFILE; \
  sh adminevents | htmlout | fileappend $REPORTMDFILE; \
  
  exit"

pandoc $REPORTMDFILE -o spreport.html