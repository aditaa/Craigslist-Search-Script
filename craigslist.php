<?php

/******************************************************************************
 * Copyright © 2011, Mike Roddewig (mike@dietfig.org).
 * All rights reserved.
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License v3 as published 
 * by the Free Software Foundation.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
******************************************************************************/
?>

<html>
<head>
<title>Craigslist Search Results</title>
</head>
<body>

<h3>Craigslist Listings</h3>
<table border="1">


<?php

$db = new PDO('sqlite:/var/db/craigslist.db');

$result = $db->query('SELECT * FROM listings ORDER BY found DESC');
$update_time = "";


while ($row = $result->fetch(PDO::FETCH_ASSOC)) {

	echo "<tr><td>";

	if ($row["new"] == 1) 
	{ 
		echo "*"; 
	}

	echo "<a href=\" ";
	echo $row["url"]; 
	echo "\">";
	echo $row["title"]; 
	echo "</a></td><td>";
	echo $row["text"];
	echo "<br><br>";
	echo "<em>Found on ";
	echo $row["found"]; 
	echo "</em></td></tr>";
	
	$update_time = $row["last_update"];
}

$result = $db->exec('UPDATE listings SET new = 0 WHERE new = 1');
$result = $db->exec('COMMIT');

?>

</table>

<h4>Last Update: <? echo $update_time; ?></h4>

</body>
</html>
