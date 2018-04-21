<?php
require_once 'class/Directory.php';

$dc = new DirectoryCrawler(true);
?>
<!DOCTYPE html>
<html>
    <head>
        <title>Tinychat Directory Crawler</title>
        <link rel="stylesheet" type="text/css" href="style.css">
    </head>
    
    
    <body>
        <div id="status">
            <?php echo "Rooms: ".count($dc->rooms).
                       " Pages crawled: ".$dc->pages_crawled; ?>
        </div>
        
        <div id="clear-fix"></div>
        
        <?php 
        foreach ($dc->rooms as $room)
        { ?>
        <div id="room-container">
            <div id="room-header"><?php echo 
            "<a href=\"https://tinychat.com/room/".$room->name."\">
                ".$room->name."</a>
                    Broadcasting: ".$room->broadcasting_count.
                    " Watching: ". $room->watching_count; ?> 
                </div>
            <?php foreach ($room->room_images() as $image)
            {
                echo "<img class=\"room_image\" src=\"$image->url\">\n";
            } ?>
        </div>
        
        <div id="clear-fix"></div>
        
        <?php } ?>

    </body>
    
    
</html>
