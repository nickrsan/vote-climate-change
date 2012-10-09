import models
import utils

states = (
	('Alabama','AL','1'),
	('Alaska','AK','2'),
	('Arizona','AZ','4'),
	('Arkansas','AR','5'),
	('California','CA','6'),
	('Colorado','CO','8'),
	('Connecticut','CT','9'),
	('Delaware','DE','10'),
	('District of Columbia','DC','11'),
	('Florida','FL','12'),
	('Georgia','GA','13'),
	('Hawaii','HI','15'),
	('Idaho','ID','16'),
	('Illinois','IL','17'),
	('Indiana','IN','18'),
	('Iowa','IA','19'),
	('Kansas','KS','20'),
	('Kentucky','KY','21'),
	('Louisiana','LA','22'),
	('Maine','ME','23'),
	('Maryland','MD','24'),
	('Massachusetts','MA','25'),
	('Michigan','MI','26'),
	('Minnesota','MN','27'),
	('Mississippi','MS','28'),
	('Missouri','MO','29'),
	('Montana','MT','30'),
	('Nebraska','NE','31'),
	('Nevada','NV','32'),
	('New Hampshire','NH','33'),
	('New Jersey','NJ','34'),
	('New Mexico','NM','35'),
	('New York','NY','36'),
	('North Carolina','NC','37'),
	('North Dakota','ND','38'),
	('Ohio','OH','39'),
	('Oklahoma','OK','40'),
	('Oregon','OR','41'),
	('Pennsylvania','PA','42'),
	('Rhode Island','RI','44'),
	('South Carolina','SC','45'),
	('South Dakota','SD','46'),
	('Tennessee','TN','47'),
	('Texas','TX','48'),
	('Utah','UT','49'),
	('Vermont','VT','50'),
	('Virginia','VA','51'),
	('Washington','WA','53'),
	('West Virginia','WV','54'),
	('Wisconsin','WI','55'),
	('Wyoming','WY','56'),
	('American Samoa','AS','60'),
	('Guam','GU','66'),
	('Northern Mariana Islands','MP','69'),
	('Puerto Rico','PR','72'),
	('Virgin Islands','VI','78'),
	('U.S. Minor Outlying Islands','XOI',0), # X means I extended this to include an abbrev
	('Federated States of Micronesia','FM','64'),
	('Marshall Islands','MH','68'),
	('Palau','PW','70'),
	('Other non-state','XOT',0), # added by nick to account for non-matching states and still provide the foreign key
)

def seed():

	print "Seeding Styles"
	style1 = models.style(name="voting_for",publisher="publisher_voting_for.django")
	style1.template_string = "I'm voting for ${candidate} because he or she has taken or has promised to take constructive action on climate change.<span>${first_name} in ${state}"
	style1.output_template = "template_voting_for.django_include"
	style1.save()

	print "Seeding Facts"
	fact1 = models.fact(statement="61 percent of undecided voters said in March 2012 that climate change is an important issue when considering their choice for president.")
	fact1.source = "http://www.climatechangecommunication.org/images/files/Policy-Support-March-2012.pdf"
	fact1.source_name = "Climate Beliefs March 2012"
	fact1.save()

	fact2 = models.fact(statement="2 out of 3 undecided voters said in March 2012 that the federal government should do more to address climate change")
	fact2.source = "http://www.climatechangecommunication.org/images/files/Policy-Support-March-2012.pdf"
	fact2.source_name = "Climate Beliefs March 2012"
	fact2.save()

	print "Seeding States"
	for state in states:
		#print "%s, %s, %s" % (state[0],state[1],state[2])
		new_state = models.state(name=state[0],abbreviation=state[1],fips_code=state[2])
		new_state.save()

	print "Seeding Candidates"

	utils.find_candidate("Barack Obama")
	obama = models.candidate.objects.get(name="Barack Obama")
	obama.state = None
	obama.save()

	utils.find_candidate("Joe Biden")
	biden = models.candidate.objects.get(pk=2)
	biden.state = None
	biden.save()

	utils.find_candidate("Jon Kyl")
	utils.find_candidate("Dianne Feinstein")
	utils.find_candidate("Joe Lieberman")
	utils.find_candidate("Tom Carper")
	utils.find_candidate("Bill Nelson")
	utils.find_candidate("Daniel Akaka")
	utils.find_candidate("Richard Lugar")
	utils.find_candidate("Olympia Snowe")
	utils.find_candidate("Ben Cardin")
	utils.find_candidate("Scott Brown")
	utils.find_candidate("Debbie Stabenow")
	utils.find_candidate("Amy Klobuchar")
	utils.find_candidate("Roger Wicker")
	utils.find_candidate("Claire McCaskill")
	utils.find_candidate("Jon Tester")
	utils.find_candidate("Ben Nelson")
	utils.find_candidate("Dean Heller")
	utils.find_candidate("Bob Menendez")
	utils.find_candidate("Jeff Bingaman")
	utils.find_candidate("Kirsten Gillibrand")
	utils.find_candidate("Kent Conrad")
	utils.find_candidate("Sherrod Brown")
	utils.find_candidate("Bob Casey")
	utils.find_candidate("Sheldon Whitehouse")
	utils.find_candidate("Bob Corker")
	utils.find_candidate("Kay Bailey Hutchison")
	utils.find_candidate("Orrin Hatch")
	utils.find_candidate("Bernie Sanders")
	utils.find_candidate("Jim Webb")
	utils.find_candidate("Maria Cantwell")
	utils.find_candidate("Joe Manchin")
	utils.find_candidate("Herb Kohl")
	utils.find_candidate("John Barrasso")

if __name__ == "__main__":
	seed()