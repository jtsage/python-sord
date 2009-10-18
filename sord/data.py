#!/usr/bin/python
"""
 * Static variables used through game.
 * 
 * Contains all non monster data for the game.
 * 
 * @package phpsord
 * @subpackage phpsord-data
 * @author J.T.Sage
 * @staticvar array $armor Names of available armor.
 * @staticvar array $armordef Defence added for each armor type.
 * @staticvar array $armorndef Defence needed for armor purchase.
 * @staticvar array $armorprice Price of each armor type.
 * @staticvar array $classes Types of player classes.
 * @staticvar array $flirts Flirting with violet - Charm needed, Text, Experience gained
 * @staticvar array $thebard Asking the bard to sing - Song text, Song finish, mysql operation
 * @staticvar array $weapon Names of available weapons.
 * @staticvar array $weaponnstr Strength needed for each weapon type.
 * @staticvar array $weaponprice Price of each weapon.
 * @staticvar array $weaponstr Strength added for each weapon type.
 * @staticvar array $enemies Enemies by level - Enemy Name, Enemy Weapon, Strenth, HP, Gold Gain, Experience Gain, Die Message
 * @staticvar array $forestdie Strings for use when dieing in the forest.  Very sad.
 * @staticvar array $master Master by level - Master Name, Master Weapon, Exp Needed, Speech, Ready Speech, Win Speech, HP, Strength, Defense
 * @staticvar array $masterwin Rewards for level up - HP Gain, Strength Gain, Defense Gain
"""

classes = [ "empty", "Death Knight", "Mystical", "Thief" ]

weapon      = [ "None", "Stick", "Dagger", "Short Sword", "Long Sword", "Huge Axe", "Bone Cruncer", "Twin Swords", "Power Axe", "Able's Sword", "Wan's Weapon", "Spear Of Gold", "Crystal Shard", "Niras's Teeth", "Blood Sword", "Death Sword" ]
weaponprice = [ 0, 200, 1000, 3000, 10000, 30000, 100000, 150000, 200000, 400000, 1000000, 4000000, 10000000, 40000000, 100000000, 400000000 ]
weaponstr   = [ 0, 5, 10, 20, 30, 40, 60, 80, 120, 180, 250, 350, 500, 800, 1200, 1800 ]
weaponnstr  = [ 0, 0, 0, 15, 22, 32, 44, 64, 99, 149, 224, 334, 334, 334, 334, 334 ]

armor      = [ "None", "Coat", "Heavy Coat", "Leather Vest", "Bronze Armour", "Iron Armour", "Graphite Armour", "Erdrick's Armour", "Armour of Death", "Able's Armour", "Full Body Armour", "Blood Armour", "Magin Protection", "Belar's Mail", "Golden Armour", "Armour Of Lore" ]
armorprice = [ 0, 200, 1000, 3000, 10000, 30000, 100000, 150000, 200000, 400000, 1000000, 4000000, 10000000, 40000000, 100000000, 400000000 ]
armordef   = [ 0, 1, 3, 10, 15, 25, 35, 50, 75, 100, 150, 225, 300, 400, 600, 1000 ]
armorndef  = [ 0, 0, 0, 2, 5, 10, 20, 35, 57, 92, 152, 232, 232, 232, 232, 232 ]

thebard = [ [['',''],[''],''],
	[['..."There once was a warrior, with a beard"...', '..."He had a power, yes XX was feared"...', '..."Nothing he did, could ever be wrong"...', '..."He was quick, and he was strong"...'],
		['The song makes you feel powerful!', 'YOU RECEIVE THREE MORE FOREST FIGHTS FOR TODAY!'],
		'ffight = ffight + 3'],
	[['..."There once was a woman, of exceeding fame"...', '..."She had a power, XX was her name"...', '..."Nothing she did, could ever be wrong"...', '..."She was quick, and she was strong"...' ],
		['The song makes you feel powerful!', 'YOU RECEIVE THREE MORE FOREST FIGHTS FOR TODAY!'],
		'ffight = ffight + 3'],
	[['..."Waiting in the forest, waiting for his prey"...', '..."XX didn\'t care what they would say"...', '..."He killed in the town, the lands"...', '..."He wanted evil\'s blood, on his hands"...', '..."A true man was XX, a warrior proud"...', '..."He voiced his opinions meekly, never very loud"...', '..."But he ain\'t no wimp, he took Violet to bed"...', '..."He\'s definately a man, at least that\'s what she said!"...' ],
		['The song makes you glad you are male!', 'YOU RECEIVE TWO EXTRA FOREST FIGHTS!'],
		'ffight = ffight + 2'],
	[['..."This is the story, of a bard"...', '..."Stabbed in the hand, with a shard"...', '..."They said he\'d never play, but they would rue the day"...', '..."He practiced all the time, becoming good before long"...', '..."Able got his revenge, by proving them wrong"...' ],
		['The song makes you feel sad, yet happy.', 'YOU RECEIVE TWO MORE FOREST FIGHTS FOR TODAY!' ],
		'ffight = ffight + 2'],
	[['..."Let me tell you the Legend, of the Red Dragon"...', '..."They said he was old, that his claws were saggin"...', '..."It\'s not so, don\'t be fooled"...', '..."He\'s alive and well, still killing where he ruled"...' ],
		['The song makes you feel a strange wonder, an awakening..', 'YOU RECEIVE ONE MORE FOREST FIGHT FOR TODAY!'],
		'ffight = ffight + 1'],
	[['..."The children are missing, the children are gone"...', '..."They have no pillow to lay upon,"...', '..."The hopes of the people are starting to dim"...', '..."They are gone, because the Dragon has eaten them"...' ],
		['Tears run down your face.  You swear you will avenge the children.', 'YOU RECEIVE AN EXTRA USER BATTLE FOR TODAY!'],
		'pfight = pfight + 1'],
	[['..."XX was a warrior, a man"...', '..."When he wants to do a thing, he can"...', '..."To live, to die, it\'s all the same"...', '..."But it is better to die, than live in shame"...' ],
		['The song makes you feel your heritage.', 'YOUR HIT POINTS ARE MAXED OUT!' ],
		'hp = hpmax'],
	[['..."XX has a story, that must be told"...', '..."He is already a legend, and he ain\'t even old"...', '..."He can drink a river of blood and not burst"...', '..."He can swallow a desert and never thirst"...' ],
		['The hero has inspired you, and in doing so, made you a better warrior.', 'YOUR HITPOINTS INCREASE BY ONE!'],
		'hpmax = hpmax + 1'],
	[['..."The Gods have powers, the Gods are just"...', '..."The Gods help us people, when they must"...', '..."Gods can heal the sick, even the cancered"...', '..."Pray to the Gods, and you will be answered"...' ],
		['You find yourself wishing for more money."', 'SOMEWHERE, MAGIC HAS HAPPENED!' ],
		'bank = bank * 2'],
	[['..."XX was a warrior, a queen"...', '..."She was a beauty, and she was mean"...', '..."She could melt a heart, at a glance"...', '..."And men would pay, to see her dance!"...' ],
		['The song makes you feel pretty!', 'YOU RECEIVE A CHARM POINT!' ],
		'charm = charm + 1']
	]

flirts = [[],
	[[1, '(W)ink', 5],[2, '(K)iss Her Hand', 10],[4, '(P)eck Her On The Lips', 20],[8, '(S)it Her On Your Lap', 30],[16, '(G)rab Her Backside', 40],[32, '(C)arry Her Upstairs', 40]],
	[[1, '(W)ink', 5],[2, '(F)lutter Eyelashes', 10],[4, '(D)rop Hankee', 20],[8, '(A)sk The Bard to Buy You a Drink', 30],[16, '(K)iss The Bard Soundly', 40],[32, '(C)ompletely Seduce The Bard', 40]]
	]

enemies = [[],
	[
		['Small Thief', 'Small Dagger', 6, 9, 56, 2, 'You disembowel the little thieving menace!'],
		['Rude Boy', 'Cudgel', 3, 7, 7, 3, 'You quietly watch as the very Rude Boy bleeds to death.'],
		['Old Man', 'Cane', 5, 13, 73, 4, 'You finish him off, by tripping him with his own cane.'],
		['Large Green Rat', 'Sharp Teeth', 3, 4, 32, 1, 'A well placed step ends this small rodents life.'],
		['Wild Boar', 'Sharp Tusks', 10, 9, 58, 5, 'You impale the boar between the eyes!'],
		['Ugly Old Hag', 'Garlic Breath', 6, 9, 109, 4, 'You emotionally crush the hag, by calling her ugly!'],
		['Large Mosquito', 'Blood Sucker', 2, 3, 46, 2, 'With a sharp slap, you end the Mosquitos life.'],
		['Bran The Warrior', 'Short Sword', 12, 15, 234, 10, 'After a hardy duel, Bran lies at your feet, dead.'],
		['Evil Wretch', 'Finger Nail', 7, 12, 76, 3, 'With a swift boot to her head, you kill her.'],
		['Small Bear', 'Claws', 9, 7, 154, 6, 'After a swift battle, you stand holding the Bears heart!'],
		['Small Troll', 'Uglyness', 6, 14, 87, 5, 'This battle reminds you how of how much you hate trolls.']
	],[
		['Green Python', 'Dripping Fangs', 13, 17, 80, 6, 'You tie the mighty snake\'s carcass to a tree.'],
		['Gath The Barbarian', 'Huge Spiked Club', 12, 13, 134, 9, 'You knock Gath down, ignoring his constant groaning.'],
		['Evil Wood Nymph', 'Flirtatios Behavior', 15, 10, 160, 11, 'You shudder to think of what would have happened, had you given in.'],
		['Fedrick The Limping Baboon', 'Scary Faces', 8, 23, 97, 6, 'Fredrick will never grunt in anyones face again.'],
		['Wild Man', 'Hands', 13, 14, 134, 8, 'Pitting your wisdom against his brawn has one this battle.'],
		['Brorandia The Viking', 'Hugely Spiked Mace', 21, 18, 330, 20, 'You consider this a message to her people, "STAY AWAY!".'],
		['Huge Bald Man', 'Glare From Forehead', 19, 19, 311, 16, 'It wasn\'t even a close battle, you slaughtered him.'],
		['Senile Senior Citizen', 'Crazy Ravings', 13, 11, 270, 13, 'You may have just knocked some sense into this old man.'],
		['Membrain Man', 'Strange Ooze', 10, 16, 190, 11, 'The monstrosity has been slain.'],
		['Bent River Dryad', 'Pouring Waterfall', 12, 16, 150, 9, 'You cannot resist thinking the Dryad is "All wet".'],
		['Rock Man', 'Large Stones', 8, 27, 300, 12, 'You have shattered the Rock Mans head!']
	], [
		['Lazy Bum', 'Unwashed Body Odor', 19, 29, 380, 18, '"This was a bum deal" You think to yourself.'],
		['Two Headed Rotwieler', 'Twin Barking', 18, 32, 384, 17, 'You have silenced the mutt, once and for all.'],
		['Purple Monchichi', 'Continous Whining', 14, 29, 763, 23, 'You cant help but realize you have just killed a real loser.'],
		['Bone', 'Terrible Smoke Smell', 27, 11, 432, 16, 'Now that you have killed Bone, maybe he will get a life..'],
		['Red Neck', 'Awfull Country Slang', 19, 16, 563, 19, 'The dismembered body causes a churning in your stomach.'],
		['Winged Demon Of Death', 'Red Glare', 42, 23, 830, 28, 'You cut off the Demons head, to be sure of its death.'],
		['Black Owl', 'Hooked Beak', 28, 29, 711, 26, 'A well placed blow knocks the winged creature to the ground.'],
		['Muscled Midget', 'Low Punch', 26, 19, 870, 32, 'You laugh as the small man falls to the ground.'],
		['Headbanger Of The West', 'Ear Shattering Noises', 23, 27, 245, 43, 'You slay the rowdy noise maker and destroy his evil machines.'],
		['Morbid Walker', 'Endless Walking', 28, 10, 764, 9, 'Even lying dead on its back, it is still walking.'],
		['Magical Evil Gnome', 'Spell Of Fire', 24, 25, 638, 28, 'The Gnome\'s small body is covered in a deep red blood.']
	], [
		['Death Dog', 'Teeth', 36, 52, 1150, 36, 'You rejoice as the dog wimpers for the very last time.'],
		['Weak Orc', 'Spiked Club', 27, 32, 900, 25, 'A solid blow removes the Orcs head!'],
		['Dark Elf', 'Small bow', 43, 57, 1070, 33, 'The Elf falls at your feet, dead.'],
		['Evil Hobbit', 'Smoking Pipe', 35, 95, 1240, 46, 'The Hobbit will never bother anyone again!'],
		['Short Goblin', 'Short Sword', 34, 45, 768, 24, 'A quick lunge renders him dead!'],
		['Huge Black Bear', 'Razor Claws', 67, 48, 1765, 76, 'You bearly beat the Huge Bear...'],
		['Rabid Wolf', 'Deathlock Fangs', 45, 39, 1400, 43, 'You pull the dogs lifeless body off you.'],
		['Young Wizard', 'Weak Magic', 64, 35, 1754, 64, 'This Wizard will never cast another spell!'],
		['Mud Man', 'Mud Balls', 56, 65, 870, 43, 'You chop up the Mud Man into sushi!'],
		['Death Jester', 'Horrible Jokes', 34, 46, 1343, 32, 'You feel no pity for the Jester, his jokes being as bad as they were.'],
		['Rock Man', 'Large Stones', 87, 54, 1754, 76, 'You have shattered the Rock Mans head!']
	], [
		['Pandion Knight', 'Orkos Broadsword', 64, 59, 3100, 98, 'You are elated in the knowledge that you both fought honorably.'],
		['Jabba', 'Whiplashing Tail', 61, 198, 2384, 137, 'The fat thing falls down, never to squirm again.'],
		['Manoken Sloth', 'Dripping Paws', 54, 69, 2452, 97, 'You have cut him down, spraying a neaby tree with blood.'],
		['Trojan Warrior', 'Twin Swords', 73, 87, 3432, 154, 'You watch, as the ants claim his body.'],
		['Misfit The Ugly', 'Strange Ideas', 75, 89, 2563, 120, 'You cut him cleanly down the middle, in a masterfull stroke.'],
		['George Of The Jungle', 'Echoing Screams', 56, 43, 2230, 128, 'You thought the story of George was a myth, until now.'],
		['Silent Death', 'Pale Smoke', 113, 98, 4711, 230, 'Instead of spilling blood, the creature seems filled with only air.'],
		['Bald Medusa', 'Glare Of Stone', 78, 120, 4000, 256, 'You are lucky you didnt look at her... Man was she ugly!'],
		['Black Alligator', 'Extra Sharp Teeth', 65, 65, 3245, 123, 'With a single stroke, you sever the creatures head right off.'],
		['Clancy, Son Of Emporor Len Spiked Bull Whip', 52, 324, 4764, 324, 'Its a pity so many new warriors get so proud.'],
		['Black Sorcerer', 'Spell Of Lightning', 86, 25, 2838, 154, 'Thats the last spell this Sorcerer will ever cast!']
	], [
		['Iron Warrior', '3 Iron', 100, 253, 6542, 364, 'You have bent the Iron warriors Iron!'],
		['Black Soul', 'Black Candle', 112, 432, 5865, 432, 'You have released the black soul.'],
		['Gold Man', 'Rock Arm', 86, 354, 8964, 493, 'You kick the body of the Gold man to reveal some change..'],
		['Screaming Zombie', 'Gaping Mouth Full Of Teeth', 98, 286, 5322, 354, 'The battle has rendered the zombie even more unatractive then he was.'],
		['Satans Helper', 'Pack Of Lies', 112, 165, 7543, 453, 'Apparently you have seen through the Devils evil tricks'],
		['Wild Stallion', 'Hoofs', 78, 245, 4643, 532, 'You only wish you could have spared the animals life.'],
		['Belar', 'Fists Of Rage', 120, 352, 9432, 565, 'Not even Belar can stop you!'],
		['Empty Armour', 'Cutting Wind', 67, 390, 6431, 432, 'The whole battle leaves you with a strange chill.'],
		['Raging Lion', 'Teeth And Claws', 98, 274, 3643, 365, 'You rip the jaw bone off the magnificient animal!'],
		['Huge Stone Warrior', 'Rock Fist', 112, 232, 4942, 543, 'There is nothing left of the stone warrior, except a few pebbles.'],
		['Magical Evil Gnome', 'Spell Of Fire', 89, 234, 6384, 321, 'The Gnomes small body is covered in a deep red blood.']
	], [
		['Emporer Len', 'Lightning Bull Whip', 210, 432, 12043, 764, 'His last words were.. "I have failed to avenge my son."'],
		['Night Hawk', 'Blood Red Talons', 220, 675, 10433, 686, 'Your last swing pulls the bird out of the air, landing him at your feet'],
		['Charging Rhinoceros', 'Rather Large Horn', 187, 454, 9853, 654, 'You finally fell the huge beast, not without a few scratches.'],
		['Goblin Pygmy', 'Death Squeeze', 165, 576, 13252, 754, 'You laugh at the little Goblin\'s puny attack.'],
		['Goliath', 'Six Fingered Fist', 243, 343, 14322, 898, 'Now you know how David felt...'],
		['Angry Liontaur', 'Arms And Teeth', 187, 495, 13259, 753, 'You have laid this mythical beast to rest.'],
		['Fallen Angel', 'Throwing Halos', 154, 654, 12339, 483, 'You slay the Angel, then watch as it gets sucked down into the ground.'],
		['Wicked Wombat', 'The Dark Wombats Curse', 198, 464, 13283, 786, 'It\'s hard to believe a little wombat like that could be so much trouble'],
		['Massive Dinosaur', 'Gaping Jaws', 200, 986, 16753, 1204, 'The earth shakes as the huge beast falls to the ground.'],
		['Swiss Butcher', 'Meat Cleaver', 230, 453, 8363, 532, 'You\'re glad you won...You really didn\'t want the haircut..'],
		['Death Gnome', 'Touch Of Death', 270, 232, 10000, 654, 'You watch as the animals pick away at his flesh.']
	], [
		['Screeching Witch', 'Spell Of Ice', 300, 674, 19753, 2283, 'You have silenced the witch\'s infernal screeching.'],
		['Rundorig', 'Poison Claws', 330, 675, 17853, 2748, 'Rundorig, once your friend, now lays dead before you.'],
		['Wheeler', 'Annoying Laugh', 250, 786, 23433, 1980, 'You rip the wheeler\'s wheels clean off!'],
		['Death Knight', 'Huge Silver Sword', 287, 674, 21923, 4282, 'The Death knight finally falls, not only wounded, but dead.'],
		['Werewolf', 'Fangs', 230, 543, 19474, 3853, 'You have slaughtered the Werewolf. You didn\'t even need a silver bullet'],
		['Fire Ork', 'FireBall', 267, 674, 24933, 3942, 'You have put out this Fire Orks flame!'],
		['Wans Beast', 'Crushing Embrace', 193, 1243, 17141, 2432, 'The hairy thing has finally stopped moving.'],
		['Lord Mathese', 'Fencing Sword', 245, 875, 24935, 2422, 'You have wiped the sneer off his face once and for all.'],
		['King Vidion', 'Long Sword Of Death', 400, 1243, 28575, 6764, 'You feel lucky to have lived, things could have gone sour..'],
		['Baby Dragon', 'Dragon Smoke', 176, 2322, 25863, 3675, 'This Baby Dragon will never grow up.'],
		['Death Gnome', 'Touch Of Death', 356, 870, 31638, 2300, 'You watch as the animals pick away at his flesh.']
	], [
		['Pink Elephant', 'Stomping', 434, 1232, 33844, 7843, 'You have witnessed the Pink Elephant...And you aren\'t even drunk!'],
		['Gwendolens Nightmare', 'Dreams', 490, 764, 35846, 8232, 'This is the first Nightmare you have put to sleep.'],
		['Flying Cobra', 'Poison Fangs', 400, 1123, 37694, 8433, 'The creature falls to the ground with a sickening thud.'],
		['Rentakis Pet', 'Gaping Maw', 556, 987, 37584, 9854, 'You vow to find Rentaki and tell him what you think about his new pet.'],
		['Ernest Brown', 'Knee', 432, 2488, 34833, 9754, 'Ernest has finally learned his lesson it seems.'],
		['Scallian Rap', 'Way Of Hurting People', 601, 788, 22430, 6784, 'Scallians dead...Looks like you took out the trash...'],
		['Apeman', 'Hairy Hands', 498, 1283, 38955, 7202, 'The battle is over...Nothing is left but blood and hair.'],
		['Hemo-Glob', 'Weak Insults', 212, 1232, 27853, 4432, 'The battle is over.. And you really didn\'t find him particularly scary.'],
		['FrankenMoose', 'Butting Head', 455, 1221, 31221, 5433, 'That Moose was a perversion of nature!'],
		['Earth Shaker', 'Earthquake', 767, 985, 37565, 7432, 'The battle is over...And it looks like you shook him up...'],
		['Gollums Wrath', 'Ring Of Invisibility', 621, 2344, 42533, 13544, 'Gollums ring apparently wasn\'t powerfull enough.']
	], [
		['Toraks Son, Korak', 'Sword Of Lightning', 921, 1384, 46575, 13877, 'You have slain the son of a God! You ARE great!'],
		['Brand The Wanderer', 'Fighting Quarter Staff', 643, 2788, 38755, 13744, 'Brand will wander no more.'],
		['The Grimest Reaper', 'White Sickle', 878, 1674, 39844, 14237, 'You have killed that which was already dead. Odd.'],
		['Death Dealer', 'Stare Of Paralization', 765, 1764, 47333, 13877, 'The Death Dealer has been has been delt his last hand.'],
		['Tiger Of The Deep Jungle', 'Eye Of The Tiger', 587, 3101, 43933, 9766, 'The Tiger\'s cubs weep over their dead mother.'],
		['Sweet Looking Little Girl', 'Demon Strike', 989, 1232, 52322, 14534, 'If it wasn\'t for her manners, you might have got along with her.'],
		['Floating Evil Eye', 'Evil Stare', 776, 2232, 43233, 13455, 'You really didn\'t like the look of that Eye...'],
		['Slock', 'Swamp Slime', 744, 1675, 56444, 14333, 'Walking away fromm the battle, you nearly slip on the thing\'s slime.'],
		['Adult Gold Dragon', 'Dragon Fire', 565, 3222, 56444, 15364, 'He was strong, but you were stronger.'],
		['Kill Joy', 'Terrible Stench', 988, 3222, 168844, 25766, 'Kill Joy has fallen, and can\'t get up.'],
		['Black Sorcerer', 'Spell Of Lightning', 86, 25, 2838, 187, 'Thats the last spell this Sorcerer will ever cast!']
	], [
		['Gorma The Leper', 'Contagous Desease', 1132, 2766, 168774, 26333, 'It looks like the lepers fighting stratagy has fallen apart..'],
		['Shogun Warrior', 'Japanese Nortaki', 1143, 3878, 165433, 26555, 'He was tough, but not nearly tough enough.'],
		['Apparently Weak Old Woman', '*GODS HAMMER*', 1543, 1878, 173522, 37762, 'You pull back the old womans hood, to reveal an eyeless skull.'],
		['Ables Creature', 'Bear Hug', 985, 2455, 176775, 28222, 'That was a mighty creature. Created by a mighty man.'],
		['White Bear Of Lore', 'Snow Of Death', 1344, 1875, 65544, 16775, 'The White Bear Of Lore DOES exist you\'ve found. Too bad it\'s now dead.'],
		['Mountain', 'Landslide', 1544, 1284, 186454, 38774, 'You have knocked the mountain to the ground. Now it IS the ground.'],
		['Sheena The Shapechanger', 'Deadly Illusions', 1463, 1898, 165755, 26655, 'Sheena is now a quivering mass of flesh. Her last shapechange.'],
		['ShadowStormWarrior', 'Mystical Storm', 1655, 2767, 162445, 26181, 'The storm is over, and the sunshine greets you as the victor.'],
		['Madman', 'Chant Of Insanity', 1265, 1764, 149564, 25665, 'Madman must have been mad to think he could beat you!'],
		['Vegetable Creature', 'Pickled Cabbage', 111, 172, 4838, 2187, 'For once you finished off your greens...'],
		['Cyclops Warrior', 'Fire Eye', 1744, 2899, 204000, 49299, 'The dead Cyclop\'s one eye stares at you blankly.']
	], [
		['Corinthian Giant', 'De-rooted Tree', 2400, 2544, 336643, 60333, 'You hope the giant has brothers, more sport for you.'],
		['The Screaming Eunich', 'High Pitched Voice', 1488, 2877, 197888, 78884, 'If it wasn\'t for his ugly features, you thought he looked female.'],
		['Black Warlock', 'Satanic Choruses', 1366, 2767, 168483, 58989, 'You have slain Satan\'s only son.'],
		['Kal Torak', 'Cthrek Goru', 876, 6666, 447774, 94663, 'You have slain a God! You are the ultimate warrior!'],
		['The Mighty Shadow', 'Shadow Axe', 1633, 2332, 176333, 51655, 'The mighty Shadow is now only a Shadow of his former self.'],
		['Black Unicorn', 'Shredding Horn', 1899, 1587, 336693, 41738, 'You have felled the Unicorn, not the first, not the last.'],
		['Mutated Black Widow', 'Venom Bite', 2575, 1276, 434370, 98993, 'A well placed stomp ends this Spider\'s life.'],
		['Humongous Black Wyre', 'Death Talons', 1166, 3453, 653834, 76000, 'The Wyre\'s dead carcass covers the whole field!'],
		['The Wizard Of Darkness', 'Chant Of Insanity', 1497, 1383, 224964, 39878, 'This Wizard of Darkness will never bother you again'],
		['Great Ogre Of The North', 'Spiked Steel Mace', 1800, 2878, 524838, 112833, 'No one is going to call him The "Great" Ogre Of The North again.']
	]]

masters = [[],
	[
		'Halder', 'Short Sword', 100,
		['"Hi there.  Although I may not look muscular, I ain\'t all', 'that weak.  You cannot advance to another Master until you', 'can best me in battle.  I don\'t really have any advice', 'except wear a groin cup at all times.  I learned the hard', 'way."'],
		'"Gee, your muscles are getting bigger than mine...',
		'Belar!!!  You are truly a great warrior!',
		30, 15, 3
	], [
		'Barak', 'Battle Axe', 400,
		['"You are now level two, and a respected warrior.', 'Try talking to the Bartender, he will see you now.  He', 'is a worthy asset... Remember, your ultimate goal is', 'to reach Ultimate Warrior status, which is level twelve."'],
		'"You know, you are actually getting pretty good with that thing..."',
		'Children Of Mara!!!  You have bested me??!',
		45, 22, 6
	], [
		'Aragorn', 'Twin Swords', 1000,
		['"You are now level three, and you are actually becoming', 'well known in the realm.  I heard your name being mentioned', 'by Violet.... Ye Gods she\'s hot...."'],
		'"You have learned everything I can teach you."',
		'Torak\'s Eye!!!  You are a great warrior!',
		65, 32, 11
	], [
		'Olodrin', 'Power Axe', 4000,
		['"You are now level four.  But don\'t get cocky - There', 'are many in the realm that could kick your...  Nevermind,', 'I\'m just not good at being insperational."'],
		'"You\'re becoming a very skilled warrior."',
		'Ye Gods!!  You are a master warrior!',
		95, 44, 21
	], [
		'Sandtiger', 'Blessed Sword', 10000,
		['"You are now level five..Not bad...Not bad at all..', 'I am called Sandtiger - Because.. Actually I can\'t', 'remember why people call me that.  Oh - Don\'t pay attention"', 'to that stupid bartender - I could make a much better one.'],
		'"Gee - You really know how to handle your shaft!"',
		'Very impressive...Very VERY impressive.',
		145, 64, 36
	], [
		'Sparhawk', 'Double Bladed Sword', 40000,
  		['"You are level six!  Vengeance is yours!', 'You can now beat up on all those young punks that made', 'fun of you when you were level 1.  This patch?  Oh - I', 'lost my eye when I fell on my sword after tripping', 'over a gopher.  If you tell anyone this, I\'ll hunt you', 'down.'],
		'"You\'re getting the hang of it now!"',
		'This Battle is yours...You have fought with honor.',
		220, 99, 58
	], [
		'Atsuko Sensei', 'Huge Curved Blade', 100000,
		['"Even in my country,  you would be considered a good', 'warrior.  But you have much to learn.  Remember to', 'always respect your teachers, for it is right."'],
		'"You are ready to be tested on the battle field!"',
		'Even though you beat me, I am proud of you.',
		345, 149, 93
	], [
		'Aladdin', 'Shiny Lamp', 400000,
		['"You are now level eight.  Remember, do not use your', 'great strength in bullying the other warriors.  Do not', 'be a braggart.  Be humble, and remember, honor is everything."' ],
		'"You REALLY know how to use your weapon!!!"',
		'I don\'t need a genie to see that you beat me, man!',
		530, 224, 153
	], [
		'Prince Caspian', 'Flashing Rapier', 1000000,
		['"You are now level nine.  You have traveled far on the', 'road of hardships,  but what doesn\'t kill you, only', 'makes you stronger.  Never stop fighting.' ],
		'"Something tells me you are as good as I am now.."',
		'Good show, chap!  Jolly good show!',
		780, 334, 233
	], [
		'Gabdalf', 'Huge Fireballs', 4000000,
		['"You are now level ten.. A true honor!', 'Do not stop now... You may be the one to rid the realm', 'of the Red Dragon yet...  Only two more levels to go', 'until you are the greatest warrior in the land."' ],
		'"You\'re becoming a very skilled warrior.',
		'Torak\'s Tooth!  You are great!', 
		1130, 484, 353
	], [
		'Turgon', 'Ables Sword', 10000000,
		['"I am Turgon, son.  The greatest warrior in the realm.', 'You are a great warrior, and if you best me, you must', 'find and kill the Red Dragon.  I have every faith in you."' ],
		'"You are truly the BEST warrior in the realm."',
		'You are a master warrior!',
		1680, 684, 503
	]]

masterwin = [[],
	[10, 5, 2],
	[15, 7, 3],
	[20, 10, 5],
	[30, 12, 10],
	[50, 20, 15],
	[75, 35, 22],
	[125, 50, 35],
	[185, 75, 60],
	[250, 110, 80],
	[350, 150, 120],
	[550, 200, 150]]

forestdie = [
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
	'The banker is already looking for `g\'s next of kin'];

