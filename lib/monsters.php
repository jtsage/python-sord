<?php
/**
 * Static variables used through game.
 * 
 * Contains all monster / master data for the game.
 * 
 * @package phpsord
 * @subpackage phpsord-data
 * @author J.T.Sage
 * @staticvar array $enemies Enemies by level - Enemy Name, Enemy Weapon, Strenth, HP, Gold Gain, Experience Gain, Die Message
 * @staticvar array $forestdie Strings for use when dieing in the forest.  Very sad.
 * @staticvar array $master Master by level - Master Name, Master Weapon, Exp Needed, Speech, Ready Speech, Win Speech, HP, Strength, Defense
 * @staticvar array $masterwin Rewards for level up - HP Gain, Strength Gain, Defense Gain
 */

$enemies = array(
	1 => array(
		array ('Small Thief', 'Small Dagger', 6, 9, 56, 2, 'You disembowel the little thieving menace!'),
		array ('Rude Boy', 'Cudgel', 3, 7, 7, 3, 'You quietly watch as the very Rude Boy bleeds to death.'),
		array ('Old Man', 'Cane', 5, 13, 73, 4, 'You finish him off, by tripping him with his own cane.'),
		array ('Large Green Rat', 'Sharp Teeth', 3, 4, 32, 1, 'A well placed step ends this small rodents life.'),
		array ('Wild Boar', 'Sharp Tusks', 10, 9, 58, 5, 'You impale the boar between the eyes!'),
		array ('Ugly Old Hag', 'Garlic Breath', 6, 9, 109, 4, 'You emotionally crush the hag, by calling her ugly!'),
		array ('Large Mosquito', 'Blood Sucker', 2, 3, 46, 2, 'With a sharp slap, you end the Mosquitos life.'),
		array ('Bran The Warrior', 'Short Sword', 12, 15, 234, 10, 'After a hardy duel, Bran lies at your feet, dead.'),
		array ('Evil Wretch', 'Finger Nail', 7, 12, 76, 3, 'With a swift boot to her head, you kill her.'),
		array ('Small Bear', 'Claws', 9, 7, 154, 6, 'After a swift battle, you stand holding the Bears heart!'),
		array ('Small Troll', 'Uglyness', 6, 14, 87, 5, 'This battle reminds you how of how much you hate trolls.')
	),
	2 => array (
		array ('Green Python', 'Dripping Fangs', 13, 17, 80, 6, 'You tie the mighty snake\'s carcass to a tree.'),
		array ('Gath The Barbarian', 'Huge Spiked Club', 12, 13, 134, 9, 'You knock Gath down, ignoring his constant groaning.'),
		array ('Evil Wood Nymph', 'Flirtatios Behavior', 15, 10, 160, 11, 'You shudder to think of what would have happened, had you given in.'),
		array ('Fedrick The Limping Baboon', 'Scary Faces', 8, 23, 97, 6, 'Fredrick will never grunt in anyones face again.'),
		array ('Wild Man', 'Hands', 13, 14, 134, 8, 'Pitting your wisdom against his brawn has one this battle.'),
		array ('Brorandia The Viking', 'Hugely Spiked Mace', 21, 18, 330, 20, 'You consider this a message to her people, "STAY AWAY!".'),
		array ('Huge Bald Man', 'Glare From Forehead', 19, 19, 311, 16, 'It wasn\'t even a close battle, you slaughtered him.'),
		array ('Senile Senior Citizen', 'Crazy Ravings', 13, 11, 270, 13, 'You may have just knocked some sense into this old man.'),
		array ('Membrain Man', 'Strange Ooze', 10, 16, 190, 11, 'The monstrosity has been slain.'),
		array ('Bent River Dryad', 'Pouring Waterfall', 12, 16, 150, 9, 'You cannot resist thinking the Dryad is "All wet".'),
		array ('Rock Man', 'Large Stones', 8, 27, 300, 12, 'You have shattered the Rock Mans head!')
	),
	3 => array (
		array ('Lazy Bum', 'Unwashed Body Odor', 19, 29, 380, 18, '"This was a bum deal" You think to yourself.'),
		array ('Two Headed Rotwieler', 'Twin Barking', 18, 32, 384, 17, 'You have silenced the mutt, once and for all.'),
		array ('Purple Monchichi', 'Continous Whining', 14, 29, 763, 23, 'You cant help but realize you have just killed a real loser.'),
		array ('Bone', 'Terrible Smoke Smell', 27, 11, 432, 16, 'Now that you have killed Bone, maybe he will get a life..'),
		array ('Red Neck', 'Awfull Country Slang', 19, 16, 563, 19, 'The dismembered body causes a churning in your stomach.'),
		array ('Winged Demon Of Death', 'Red Glare', 42, 23, 830, 28, 'You cut off the Demons head, to be sure of its death.'),
		array ('Black Owl', 'Hooked Beak', 28, 29, 711, 26, 'A well placed blow knocks the winged creature to the ground.'),
		array ('Muscled Midget', 'Low Punch', 26, 19, 870, 32, 'You laugh as the small man falls to the ground.'),
		array ('Headbanger Of The West', 'Ear Shattering Noises', 23, 27, 245, 43, 'You slay the rowdy noise maker and destroy his evil machines.'),
		array ('Morbid Walker', 'Endless Walking', 28, 10, 764, 9, 'Even lying dead on its back, it is still walking.'),
		array ('Magical Evil Gnome', 'Spell Of Fire', 24, 25, 638, 28, 'The Gnome\'s small body is covered in a deep red blood.')
	),
	4 => array (
		array ('Death Dog', 'Teeth', 36, 52, 1150, 36, 'You rejoice as the dog wimpers for the very last time.'),
		array ('Weak Orc', 'Spiked Club', 27, 32, 900, 25, 'A solid blow removes the Orcs head!'),
		array ('Dark Elf', 'Small bow', 43, 57, 1070, 33, 'The Elf falls at your feet, dead.'),
		array ('Evil Hobbit', 'Smoking Pipe', 35, 95, 1240, 46, 'The Hobbit will never bother anyone again!'),
		array ('Short Goblin', 'Short Sword', 34, 45, 768, 24, 'A quick lunge renders him dead!'),
		array ('Huge Black Bear', 'Razor Claws', 67, 48, 1765, 76, 'You bearly beat the Huge Bear...'),
		array ('Rabid Wolf', 'Deathlock Fangs', 45, 39, 1400, 43, 'You pull the dogs lifeless body off you.'),
		array ('Young Wizard', 'Weak Magic', 64, 35, 1754, 64, 'This Wizard will never cast another spell!'),
		array ('Mud Man', 'Mud Balls', 56, 65, 870, 43, 'You chop up the Mud Man into sushi!'),
		array ('Death Jester', 'Horrible Jokes', 34, 46, 1343, 32, 'You feel no pity for the Jester, his jokes being as bad as they were.'),
		array ('Rock Man', 'Large Stones', 87, 54, 1754, 76, 'You have shattered the Rock Mans head!')
	),
	5 => array (
		array ('Pandion Knight', 'Orkos Broadsword', 64, 59, 3100, 98, 'You are elated in the knowledge that you both fought honorably.'),
		array ('Jabba', 'Whiplashing Tail', 61, 198, 2384, 137, 'The fat thing falls down, never to squirm again.'),
		array ('Manoken Sloth', 'Dripping Paws', 54, 69, 2452, 97, 'You have cut him down, spraying a neaby tree with blood.'),
		array ('Trojan Warrior', 'Twin Swords', 73, 87, 3432, 154, 'You watch, as the ants claim his body.'),
		array ('Misfit The Ugly', 'Strange Ideas', 75, 89, 2563, 120, 'You cut him cleanly down the middle, in a masterfull stroke.'),
		array ('George Of The Jungle', 'Echoing Screams', 56, 43, 2230, 128, 'You thought the story of George was a myth, until now.'),
		array ('Silent Death', 'Pale Smoke', 113, 98, 4711, 230, 'Instead of spilling blood, the creature seems filled with only air.'),
		array ('Bald Medusa', 'Glare Of Stone', 78, 120, 4000, 256, 'You are lucky you didnt look at her... Man was she ugly!'),
		array ('Black Alligator', 'Extra Sharp Teeth', 65, 65, 3245, 123, 'With a single stroke, you sever the creatures head right off.'),
		array ('Clancy, Son Of Emporor Len Spiked Bull Whip', 52, 324, 4764, 324, 'Its a pity so many new warriors get so proud.'),
		array ('Black Sorcerer', 'Spell Of Lightning', 86, 25, 2838, 154, 'Thats the last spell this Sorcerer will ever cast!')
	),
	6 => array (
		array ('Iron Warrior', '3 Iron', 100, 253, 6542, 364, 'You have bent the Iron warriors Iron!'),
		array ('Black Soul', 'Black Candle', 112, 432, 5865, 432, 'You have released the black soul.'),
		array ('Gold Man', 'Rock Arm', 86, 354, 8964, 493, 'You kick the body of the Gold man to reveal some change..'),
		array ('Screaming Zombie', 'Gaping Mouth Full Of Teeth', 98, 286, 5322, 354, 'The battle has rendered the zombie even more unatractive then he was.'),
		array ('Satans Helper', 'Pack Of Lies', 112, 165, 7543, 453, 'Apparently you have seen through the Devils evil tricks'),
		array ('Wild Stallion', 'Hoofs', 78, 245, 4643, 532, 'You only wish you could have spared the animals life.'),
		array ('Belar', 'Fists Of Rage', 120, 352, 9432, 565, 'Not even Belar can stop you!'),
		array ('Empty Armour', 'Cutting Wind', 67, 390, 6431, 432, 'The whole battle leaves you with a strange chill.'),
		array ('Raging Lion', 'Teeth And Claws', 98, 274, 3643, 365, 'You rip the jaw bone off the magnificient animal!'),
		array ('Huge Stone Warrior', 'Rock Fist', 112, 232, 4942, 543, 'There is nothing left of the stone warrior, except a few pebbles.'),
		array ('Magical Evil Gnome', 'Spell Of Fire', 89, 234, 6384, 321, 'The Gnomes small body is covered in a deep red blood.')
	),
	7 => array (
		array ('Emporer Len', 'Lightning Bull Whip', 210, 432, 12043, 764, 'His last words were.. "I have failed to avenge my son."'),
		array ('Night Hawk', 'Blood Red Talons', 220, 675, 10433, 686, 'Your last swing pulls the bird out of the air, landing him at your feet'),
		array ('Charging Rhinoceros', 'Rather Large Horn', 187, 454, 9853, 654, 'You finally fell the huge beast, not without a few scratches.'),
		array ('Goblin Pygmy', 'Death Squeeze', 165, 576, 13252, 754, 'You laugh at the little Goblin\'s puny attack.'),
		array ('Goliath', 'Six Fingered Fist', 243, 343, 14322, 898, 'Now you know how David felt...'),
		array ('Angry Liontaur', 'Arms And Teeth', 187, 495, 13259, 753, 'You have laid this mythical beast to rest.'),
		array ('Fallen Angel', 'Throwing Halos', 154, 654, 12339, 483, 'You slay the Angel, then watch as it gets sucked down into the ground.'),
		array ('Wicked Wombat', 'The Dark Wombats Curse', 198, 464, 13283, 786, 'It\'s hard to believe a little wombat like that could be so much trouble'),
		array ('Massive Dinosaur', 'Gaping Jaws', 200, 986, 16753, 1204, 'The earth shakes as the huge beast falls to the ground.'),
		array ('Swiss Butcher', 'Meat Cleaver', 230, 453, 8363, 532, 'You\'re glad you won...You really didn\'t want the haircut..'),
		array ('Death Gnome', 'Touch Of Death', 270, 232, 10000, 654, 'You watch as the animals pick away at his flesh.')
	),
	8 => array (
		array ('Screeching Witch', 'Spell Of Ice', 300, 674, 19753, 2283, 'You have silenced the witch\'s infernal screeching.'),
		array ('Rundorig', 'Poison Claws', 330, 675, 17853, 2748, 'Rundorig, once your friend, now lays dead before you.'),
		array ('Wheeler', 'Annoying Laugh', 250, 786, 23433, 1980, 'You rip the wheeler\'s wheels clean off!'),
		array ('Death Knight', 'Huge Silver Sword', 287, 674, 21923, 4282, 'The Death knight finally falls, not only wounded, but dead.'),
		array ('Werewolf', 'Fangs', 230, 543, 19474, 3853, 'You have slaughtered the Werewolf. You didn\'t even need a silver bullet'),
		array ('Fire Ork', 'FireBall', 267, 674, 24933, 3942, 'You have put out this Fire Orks flame!'),
		array ('Wans Beast', 'Crushing Embrace', 193, 1243, 17141, 2432, 'The hairy thing has finally stopped moving.'),
		array ('Lord Mathese', 'Fencing Sword', 245, 875, 24935, 2422, 'You have wiped the sneer off his face once and for all.'),
		array ('King Vidion', 'Long Sword Of Death', 400, 1243, 28575, 6764, 'You feel lucky to have lived, things could have gone sour..'),
		array ('Baby Dragon', 'Dragon Smoke', 176, 2322, 25863, 3675, 'This Baby Dragon will never grow up.'),
		array ('Death Gnome', 'Touch Of Death', 356, 870, 31638, 2300, 'You watch as the animals pick away at his flesh.')
	),
	9 => array (
		array ('Pink Elephant', 'Stomping', 434, 1232, 33844, 7843, 'You have witnessed the Pink Elephant...And you aren\'t even drunk!'),
		array ('Gwendolens Nightmare', 'Dreams', 490, 764, 35846, 8232, 'This is the first Nightmare you have put to sleep.'),
		array ('Flying Cobra', 'Poison Fangs', 400, 1123, 37694, 8433, 'The creature falls to the ground with a sickening thud.'),
		array ('Rentakis Pet', 'Gaping Maw', 556, 987, 37584, 9854, 'You vow to find Rentaki and tell him what you think about his new pet.'),
		array ('Ernest Brown', 'Knee', 432, 2488, 34833, 9754, 'Ernest has finally learned his lesson it seems.'),
		array ('Scallian Rap', 'Way Of Hurting People', 601, 788, 22430, 6784, 'Scallians dead...Looks like you took out the trash...'),
		array ('Apeman', 'Hairy Hands', 498, 1283, 38955, 7202, 'The battle is over...Nothing is left but blood and hair.'),
		array ('Hemo-Glob', 'Weak Insults', 212, 1232, 27853, 4432, 'The battle is over.. And you really didn\'t find him particularly scary.'),
		array ('FrankenMoose', 'Butting Head', 455, 1221, 31221, 5433, 'That Moose was a perversion of nature!'),
		array ('Earth Shaker', 'Earthquake', 767, 985, 37565, 7432, 'The battle is over...And it looks like you shook him up...'),
		array ('Gollums Wrath', 'Ring Of Invisibility', 621, 2344, 42533, 13544, 'Gollums ring apparently wasn\'t powerfull enough.')
	),
	10 => array (
		array ('Toraks Son, Korak', 'Sword Of Lightning', 921, 1384, 46575, 13877, 'You have slain the son of a God! You ARE great!'),
		array ('Brand The Wanderer', 'Fighting Quarter Staff', 643, 2788, 38755, 13744, 'Brand will wander no more.'),
		array ('The Grimest Reaper', 'White Sickle', 878, 1674, 39844, 14237, 'You have killed that which was already dead. Odd.'),
		array ('Death Dealer', 'Stare Of Paralization', 765, 1764, 47333, 13877, 'The Death Dealer has been has been delt his last hand.'),
		array ('Tiger Of The Deep Jungle', 'Eye Of The Tiger', 587, 3101, 43933, 9766, 'The Tiger\'s cubs weep over their dead mother.'),
		array ('Sweet Looking Little Girl', 'Demon Strike', 989, 1232, 52322, 14534, 'If it wasn\'t for her manners, you might have got along with her.'),
		array ('Floating Evil Eye', 'Evil Stare', 776, 2232, 43233, 13455, 'You really didn\'t like the look of that Eye...'),
		array ('Slock', 'Swamp Slime', 744, 1675, 56444, 14333, 'Walking away fromm the battle, you nearly slip on the thing\'s slime.'),
		array ('Adult Gold Dragon', 'Dragon Fire', 565, 3222, 56444, 15364, 'He was strong, but you were stronger.'),
		array ('Kill Joy', 'Terrible Stench', 988, 3222, 168844, 25766, 'Kill Joy has fallen, and can\'t get up.'),
		array ('Black Sorcerer', 'Spell Of Lightning', 86, 25, 2838, 187, 'Thats the last spell this Sorcerer will ever cast!')
	),
	11 => array (
		array ('Gorma The Leper', 'Contagous Desease', 1132, 2766, 168774, 26333, 'It looks like the lepers fighting stratagy has fallen apart..'),
		array ('Shogun Warrior', 'Japanese Nortaki', 1143, 3878, 165433, 26555, 'He was tough, but not nearly tough enough.'),
		array ('Apparently Weak Old Woman', '*GODS HAMMER*', 1543, 1878, 173522, 37762, 'You pull back the old womans hood, to reveal an eyeless skull.'),
		array ('Ables Creature', 'Bear Hug', 985, 2455, 176775, 28222, 'That was a mighty creature. Created by a mighty man.'),
		array ('White Bear Of Lore', 'Snow Of Death', 1344, 1875, 65544, 16775, 'The White Bear Of Lore DOES exist you\'ve found. Too bad it\'s now dead.'),
		array ('Mountain', 'Landslide', 1544, 1284, 186454, 38774, 'You have knocked the mountain to the ground. Now it IS the ground.'),
		array ('Sheena The Shapechanger', 'Deadly Illusions', 1463, 1898, 165755, 26655, 'Sheena is now a quivering mass of flesh. Her last shapechange.'),
		array ('ShadowStormWarrior', 'Mystical Storm', 1655, 2767, 162445, 26181, 'The storm is over, and the sunshine greets you as the victor.'),
		array ('Madman', 'Chant Of Insanity', 1265, 1764, 149564, 25665, 'Madman must have been mad to think he could beat you!'),
		array ('Vegetable Creature', 'Pickled Cabbage', 111, 172, 4838, 2187, 'For once you finished off your greens...'),
		array ('Cyclops Warrior', 'Fire Eye', 1744, 2899, 204000, 49299, 'The dead Cyclop\'s one eye stares at you blankly.')
	),
	12 => array(
		array ('Corinthian Giant', 'De-rooted Tree', 2400, 2544, 336643, 60333, 'You hope the giant has brothers, more sport for you.'),
		array ('The Screaming Eunich', 'High Pitched Voice', 1488, 2877, 197888, 78884, 'If it wasn\'t for his ugly features, you thought he looked female.'),
		array ('Black Warlock', 'Satanic Choruses', 1366, 2767, 168483, 58989, 'You have slain Satan\'s only son.'),
		array ('Kal Torak', 'Cthrek Goru', 876, 6666, 447774, 94663, 'You have slain a God! You are the ultimate warrior!'),
		array ('The Mighty Shadow', 'Shadow Axe', 1633, 2332, 176333, 51655, 'The mighty Shadow is now only a Shadow of his former self.'),
		array ('Black Unicorn', 'Shredding Horn', 1899, 1587, 336693, 41738, 'You have felled the Unicorn, not the first, not the last.'),
		array ('Mutated Black Widow', 'Venom Bite', 2575, 1276, 434370, 98993, 'A well placed stomp ends this Spider\'s life.'),
		array ('Humongous Black Wyre', 'Death Talons', 1166, 3453, 653834, 76000, 'The Wyre\'s dead carcass covers the whole field!'),
		array ('The Wizard Of Darkness', 'Chant Of Insanity', 1497, 1383, 224964, 39878, 'This Wizard of Darkness will never bother you again'),
		array ('Great Ogre Of The North', 'Spiked Steel Mace', 1800, 2878, 524838, 112833, 'No one is going to call him The "Great" Ogre Of The North again.')
	)
);


$masters = array (
	1 => array(
		'Halder', 'Short Sword', 100,
		array ('"Hi there.  Although I may not look muscular, I ain\'t all', 'that weak.  You cannot advance to another Master until you', 'can best me in battle.  I don\'t really have any advice', 'except wear a groin cup at all times.  I learned the hard', 'way."'),
		'"Gee, your muscles are getting bigger than mine...',
		'Belar!!!  You are truly a great warrior!',
		30, 15, 3
	),
	2 => array(
		'Barak', 'Battle Axe', 400,
		array ('"You are now level two, and a respected warrior.', 'Try talking to the Bartender, he will see you now.  He', 'is a worthy asset... Remember, your ultimate goal is', 'to reach Ultimate Warrior status, which is level twelve."'),
		'"You know, you are actually getting pretty good with that thing..."',
		'Children Of Mara!!!  You have bested me??!',
		45, 22, 6
	),
	3 => array(
		'Aragorn', 'Twin Swords', 1000,
		array ('"You are now level three, and you are actually becoming', 'well known in the realm.  I heard your name being mentioned', 'by Violet.... Ye Gods she\'s hot...."'),
		'"You have learned everything I can teach you."',
		'Torak\'s Eye!!!  You are a great warrior!',
		65, 32, 11
	),
	4 => array(
		'Olodrin', 'Power Axe', 4000,
		array ('"You are now level four.  But don\'t get cocky - There', 'are many in the realm that could kick your...  Nevermind,', 'I\'m just not good at being insperational."'),
		'"You\'re becoming a very skilled warrior."',
		'Ye Gods!!  You are a master warrior!',
		95, 44, 21
	),
	5 => array(
		'Sandtiger', 'Blessed Sword', 10000,
		array ('"You are now level five..Not bad...Not bad at all..', 'I am called Sandtiger - Because.. Actually I can\'t', 'remember why people call me that.  Oh - Don\'t pay attention"', 'to that stupid bartender - I could make a much better one.'),
		'"Gee - You really know how to handle your shaft!"',
		'Very impressive...Very VERY impressive.',
		145, 64, 36
	),
	6 => array(
		'Sparhawk', 'Double Bladed Sword', 40000,
  		array ('"You are level six!  Vengeance is yours!', 'You can now beat up on all those young punks that made', 'fun of you when you were level 1.  This patch?  Oh - I', 'lost my eye when I fell on my sword after tripping', 'over a gopher.  If you tell anyone this, I\'ll hunt you', 'down.'),
		'"You\'re getting the hang of it now!"',
		'This Battle is yours...You have fought with honor.',
		220, 99, 58
	),
	7 => array(
		'Atsuko Sensei', 'Huge Curved Blade', 100000,
		array ('"Even in my country,  you would be considered a good', 'warrior.  But you have much to learn.  Remember to', 'always respect your teachers, for it is right."'),
		'"You are ready to be tested on the battle field!"',
		'Even though you beat me, I am proud of you.',
		345, 149, 93
	),
	8 => array(
		'Aladdin', 'Shiny Lamp', 400000,
		array ('"You are now level eight.  Remember, do not use your', 'great strength in bullying the other warriors.  Do not', 'be a braggart.  Be humble, and remember, honor is everything."' ),
		'"You REALLY know how to use your weapon!!!"',
		'I don\'t need a genie to see that you beat me, man!',
		530, 224, 153
	),
	9 => array(
		'Prince Caspian', 'Flashing Rapier', 1000000,
		array ('"You are now level nine.  You have traveled far on the', 'road of hardships,  but what doesn\'t kill you, only', 'makes you stronger.  Never stop fighting.' ),
		'"Something tells me you are as good as I am now.."',
		'Good show, chap!  Jolly good show!',
		780, 334, 233
	),
	10 => array(
		'Gabdalf', 'Huge Fireballs', 4000000,
		array ('"You are now level ten.. A true honor!', 'Do not stop now... You may be the one to rid the realm', 'of the Red Dragon yet...  Only two more levels to go', 'until you are the greatest warrior in the land."' ),
		'"You\'re becoming a very skilled warrior.',
		'Torak\'s Tooth!  You are great!', 
		1130, 484, 353
	),
	11 => array(
		'Turgon', 'Ables Sword', 10000000,
		array ('"I am Turgon, son.  The greatest warrior in the realm.', 'You are a great warrior, and if you best me, you must', 'find and kill the Red Dragon.  I have every faith in you."' ),
		'"You are truly the BEST warrior in the realm."',
		'You are a master warrior!',
		1680, 684, 503
	)
);

$masterwin = array(
	1 => array(10, 5, 2),
	2 => array(15, 7, 3),
	3 => array(20, 10, 5),
	4 => array(30, 12, 10),
	5 => array(50, 20, 15),
	6 => array(75, 35, 22),
	7 => array(125, 50, 35),
	8 => array(185, 75, 60),
	9 => array(250, 110, 80),
	10 => array(350, 150, 120),
	11 => array(550, 200, 150)
);

$forestdie = array(
	'"Damn, Damn, Damn!," `g roars.',
	'"I would rather gargle razor blades then be beaten by you,`n `e !," `g screams.',
	'"How the hell did you do that?!," `g shouts.',
	'"You got lucky, `e!," `g declares.',
	'"Try that again!  I\'ll decapitate you!," `g challenges.',
	'"You are definatly stronger than you look, `e," `g admits.',
	'"I am SO mad I could slice you in two!," `g  screams.',
	'"You have not seen the last of me, `e!," `g threatens.',
	'"How could a scrawny little wimp like `e best me?," `g`n  wonders aloud.',
	'"How many of you `e\'s live in that forest anyway?!,"`n  `g ponders.',
	'"Ack!  I was under the impression I was invincible. I suppose I was wrong,"`n  `g admits.',
	'"Killed by `e.  I am disgraced," grieves `g.',
	'"I\'LL BE BACK!," swears `g.',
	'"At least I wasn\'t bested by Large Rat, eh?," shrugs `g.',
	'"My goodness.  This a turn for the worse," states `g.',
	'"You never think it can happen to you...Then WHAM!," explains `g.',
	'"I think I\'m going to be sick," `g moans pitifully.',
	'"I feel ill," elucidates `g.',
	'"Well...So much for my reputation!," expounds `g.',
	'"Damnit!  I was looking for the Dark Cloak Tavern," explains`n  `g in dismay.',
	'`e devours `g raw.',
	'`e carefully burys `g.',
	'`g\'s entrails are littering the forest.',
	'Halder laughs at `g\'s plight.',
	'The banker is already looking for `g\'s next of kin');

?>


