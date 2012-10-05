import models

def seed():

	style1 = models.style(name="voting_for",publisher="publisher_voting_for.django")
	style1.template_string = "I'm voting for ${candidate} because he or she has taken or has promised to take constructive action on climate change.<span>${first_name} in ${state}"
	style1.save()

	fact1 = models.fact(statement="61 percent of undecided voters said in March 2012 that climate change is an important issue when considering their choice for president.")
	fact1.source = "http://www.climatechangecommunication.org/images/files/Policy-Support-March-2012.pdf"
	fact1.source_name = "Climate Beliefs March 2012"
	fact1.save()

	fact2 = models.fact(statement="2 out of 3 undecided voters said in March 2012 that the federal government should do more to address climate change")
	fact2.source = "http://www.climatechangecommunication.org/images/files/Policy-Support-March-2012.pdf"
	fact2.source_name = "Climate Beliefs March 2012"
	fact2.save()

if __name__ == "__main__":
	seed()