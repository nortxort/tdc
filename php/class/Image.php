<?php

class RoomImage
{    
    public $url = null;
    
    public $uid = null;
    
    public $name = null;
    
    public function __construct($image_url) 
    {
        $parts = explode('/', $image_url);
        
        $this->url = $image_url;
        $this->uid = $parts[3];
        $this->name = $parts[4];
    }
    
}
