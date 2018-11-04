<?php
require_once('Image.php');

class Room
{
    public $broadcaster_image_common = null;

    public $broadcasters_images = array();
    
    public $broadcasting_count = 0;
    
    public $description = null;
    
    public $general_icon = null;
    
    public $images = array();
    
    public $name = null;
    
    public $status = array();
    
    public $status_icon = null;
   
    public $total_users = 0;

    public $watching_count = 0;  

    public function __construct($room_data) 
    {
        if (count($room_data) > 0)
        {
            $this->broadcaster_image_common = $room_data['broadcasters_image_common'];
            $this->broadcasters_images = $room_data['broadcasters_images'];
            $this->description = $room_data['description'];
            $this->general_icon = $room_data['general_icon'];
            $this->images = $room_data['images'];
            $this->name = $room_data['name'];
            $this->status = $room_data['status'];
            $this->status_icon = $room_data['status_icon'];
            
            $users = $room_data['users'];
            $this->broadcasting_count = $users['broadcasting_count'];
            $this->watching_count = $users['watching_count'];
            $this->total_users = $this->watching_count + $this->broadcasting_count;         
        }
    }
    
    public function update_stats($users)
    {
        $this->broadcasting_count = $users['broadcasting_count'];
        $this->watching_count = $users['watching_count'];
        $this->total_users = $this->watching_count + $this->broadcasting_count; 
    }

    public function add_images($images)
    {
        if (count($images) == 1) {
            $this->images[] = $images[0];
        }
        else if (count($images) > 1) {
            $merged = array_merge($this->images, $images);
            $this->images = $merged;
        }
    }
    
    public function room_images()
    {
        $images = array();
        
        foreach ($this->images as $image_url) {
            $image = new RoomImage($image_url);
            $images[] = $image;
        }
        
        return $images;
    }
}
