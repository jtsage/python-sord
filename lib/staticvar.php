<?php
/**
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
 */

$classes = array(
	1 => "Death Knight",
	2 => "Mystical",
	3 => "Thief" );

$weapon = array( 
	0 => "None",
	1 => "Stick",
	2 => "Dagger",
	3 => "Short Sword",
	4 => "Long Sword",
	5 => "Huge Axe",
	6 => "Bone Cruncer",
	7 => "Twin Swords",
	8 => "Power Axe",
	9 => "Able's Sword",
	10 => "Wan's Weapon",
	11 => "Spear Of Gold",
	12 => "Crystal Shard",
	13 => "Niras's Teeth",
	14 => "Blood Sword",
	15 => "Death Sword");

$weaponprice = array ( 0, 200, 1000, 3000, 10000, 30000, 100000, 150000, 200000, 400000, 1000000, 4000000, 10000000, 40000000, 100000000, 400000000 );
$weaponstr   = array ( 0, 5, 10, 20, 30, 40, 60, 80, 120, 180, 250, 350, 500, 800, 1200, 1800 );
$weaponnstr  = array ( 0, 0, 0, 15, 22, 32, 44, 64, 99, 149, 224, 334, 334, 334, 334, 334 );

$armor = array(
	0 => "None",
	1 => "Coat",
	2 => "Heavy Coat",
	3 => "Leather Vest",
	4 => "Bronze Armour",
	5 => "Iron Armour",
	6 => "Graphite Armour",
	7 => "Erdrick's Armour",
	8 => "Armour of Death",
	9 => "Able's Armour",
	10 => "Full Body Armour",
	11 => "Blood Armour",
	12 => "Magin Protection",
	13 => "Belar's Mail",
	14 => "Golden Armour",
	15 => "Armour Of Lore" );

$armorprice = array ( 0, 200, 1000, 3000, 10000, 30000, 100000, 150000, 200000, 400000, 1000000, 4000000, 10000000, 40000000, 100000000, 400000000 );
$armordef   = array ( 0, 1, 3, 10, 15, 25, 35, 50, 75, 100, 150, 225, 300, 400, 600, 1000 );
$armorndef  = array ( 0, 0, 0, 2, 5, 10, 20, 35, 57, 92, 152, 232, 232, 232, 232, 232 );

$thebard = array(
	1 => array (
		array ('..."There once was a warrior, with a beard"...', '..."He had a power, yes XX was feared"...', '..."Nothing he did, could ever be wrong"...', '..."He was quick, and he was strong"...' ),
		array ('The song makes you feel powerful!', 'YOU RECEIVE THREE MORE FOREST FIGHTS FOR TODAY!'),
		'ffight = ffight + 3'
	),
	2 => array (
		array ('..."There once was a woman, of exceeding fame"...', '..."She had a power, XX was her name"...', '..."Nothing she did, could ever be wrong"...', '..."She was quick, and she was strong"...' ),
		array ('The song makes you feel powerful!', 'YOU RECEIVE THREE MORE FOREST FIGHTS FOR TODAY!'),
		'ffight = ffight + 3'
	),
	3 => array (
		array ('..."Waiting in the forest, waiting for his prey"...', '..."XX didn\'t care what they would say"...', '..."He killed in the town, the lands"...', '..."He wanted evil\'s blood, on his hands"...', '..."A true man was XX, a warrior proud"...', '..."He voiced his opinions meekly, never very loud"...', '..."But he ain\'t no wimp, he took Violet to bed"...', '..."He\'s definately a man, at least that\'s what she said!"...' ),
		array ('The song makes you glad you are male!', 'YOU RECEIVE TWO EXTRA FOREST FIGHTS!' ),
		'ffight = ffight + 2'
	),
	4 => array (
		array ('..."This is the story, of a bard"...', '..."Stabbed in the hand, with a shard"...', '..."They said he\'d never play, but they would rue the day"...', '..."He practiced all the time, becoming good before long"...', '..."Able got his revenge, by proving them wrong"...' ),
		array ('The song makes you feel sad, yet happy.', 'YOU RECEIVE TWO MORE FOREST FIGHTS FOR TODAY!' ),
		'ffight = ffight + 2'
	),
	5 => array (
		array ('..."Let me tell you the Legend, of the Red Dragon"...', '..."They said he was old, that his claws were saggin"...', '..."It\'s not so, don\'t be fooled"...', '..."He\'s alive and well, still killing where he ruled"...' ),
		array ('The song makes you feel a strange wonder, an awakening..', 'YOU RECEIVE ONE MORE FOREST FIGHT FOR TODAY!'),
		'ffight = ffight + 1'
	),
	6 => array (
		array ('..."The children are missing, the children are gone"...', '..."They have no pillow to lay upon,"...', '..."The hopes of the people are starting to dim"...', '..."They are gone, because the Dragon has eaten them"...' ),
		array ('Tears run down your face.  You swear you will avenge the children.', 'YOU RECEIVE AN EXTRA USER BATTLE FOR TODAY!'),
		'pfight = pfight + 1'
	),
	7 => array (
		array ('..."XX was a warrior, a man"...', '..."When he wants to do a thing, he can"...', '..."To live, to die, it\'s all the same"...', '..."But it is better to die, than live in shame"...' ),
		array ('The song makes you feel your heritage.', 'YOUR HIT POINTS ARE MAXED OUT!' ),
		'hp = hpmax'
	),
	8 => array (
		array ('..."XX has a story, that must be told"...', '..."He is already a legend, and he ain\'t even old"...', '..."He can drink a river of blood and not burst"...', '..."He can swallow a desert and never thirst"...' ),
		array ('The hero has inspired you, and in doing so, made you a better warrior.', 'YOUR HITPOINTS INCREASE BY ONE!'),
		'hpmax = hpmax + 1'
	),
	9 => array (
		array ('..."The Gods have powers, the Gods are just"...', '..."The Gods help us people, when they must"...', '..."Gods can heal the sick, even the cancered"...', '..."Pray to the Gods, and you will be answered"...' ),
		array ('You find yourself wishing for more money."', 'SOMEWHERE, MAGIC HAS HAPPENED!' ),
		'bank = bank * 2'
	),
	10 => array (
		array ('..."XX was a warrior, a queen"...', '..."She was a beauty, and she was mean"...', '..."She could melt a heart, at a glance"...', '..."And men would pay, to see her dance!"...' ),
		array ('The song makes you feel pretty!', 'YOU RECEIVE A CHARM POINT!' ),
		'charm = charm + 1'
	)
);


$flirts = array(
	1 => array(
		array (1, '(W)ink', 5),
		array (2, '(K)iss Her Hand', 10),
		array (4, '(P)eck Her On The Lips', 20),
		array (8, '(S)it Her On Your Lap', 30),
		array (16, '(G)rab Her Backside', 40),
		array (32, '(C)arry Her Upstairs', 40)
	),
	2 => array(
		array (1, '(W)ink', 5),
		array (2, '(F)lutter Eyelashes', 10),
		array (4, '(D)rop Hankee', 20),
		array (8, '(A)sk The Bard to Buy You a Drink', 30),
		array (16, '(K)iss The Bard Soundly', 40),
		array (32, '(C)ompletely Seduce The Bard', 40)
	)
);

?>
