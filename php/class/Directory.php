<?php
require_once('Room.php');
require_once('./web.php');

class DirectoryCrawler
{
    public $category = null;
    
    public $rooms = array();
    
    public $pages_crawled = 0;
    
    public $total_dir_users = 0;


    private $base_url = 'https://tinychat.com';
    
    private $post_url = 'https://tinychat.com/home/data';
    
    private $html_source = null;
    
    private $csrf_token = null;
    
    private $page = 0;
    
    public function __construct($crawl=False, $category='all') 
    {
        $this->category = $category;
        
        if ($crawl) {
            $this->crawl();
        }
    }
    
    public function crawl()
    {
        $webget = get($this->base_url);
        
        if ($webget['error'] == null) {
            $this->html_source = $webget['content'];
            $this->set_token();
            $this->crawler();
        }
    }
    
    private function poster($category='', $page=0)
    {
        if ($this->csrf_token != null)
        {
            $header = default_header();
            $header[] = 'X-Requested-With: XMLHttpRequest';
            $header[] = 'Content-Type: application/x-www-form-urlencoded';
            
            $post_data = 
                    '_token='.$this->csrf_token.
                    '&category='.$category.
                    '&page='.$page;
            
            $response = post($this->post_url, $post_data, $header);

            if ($response['error'] == null) {
                return $response['content'];
            }
            
            return null;
        }
    }

    private function set_token()
    {
        $doc = new DOMDocument();
        libxml_use_internal_errors(true);
        $doc->loadHTML($this->html_source);

        $token = $doc->getElementById('csrf-token');
        $this->csrf_token = $token->getAttribute('content');
    }
    
    private function data_extractor($rooms)
    {
        foreach ($rooms as $room)
        {
            $room_name = $room['name'];
            if (!array_key_exists($room_name, $this->rooms)) {
                $this->rooms[$room_name] = new Room($room);
            }
            else {
                $this->rooms[$room_name]->add_images($room['images']);
                $this->rooms[$room_name]->update_stats($room['users']);
            }
            
            $this->total_dir_users += $this->rooms[$room_name]->total_users;
        }
    }

    private function page_crawler()
    {
        $this->page = 1;

        while (True)
        {
            $page_crawler = $this->poster($this->category, $this->page);
            $json_data = json_decode($page_crawler, True);
            
            if ($page_crawler == null) {
                break;
            }
            if (count($json_data['rooms']) == 0) {
                break;
            }
            else {
                $rooms = $json_data['rooms'];
                $this->data_extractor($rooms);
                $this->page ++;
            } 
        }
        
        $this->pages_crawled = $this->page - 1;     
    }

    private function crawler()
    {
        $first_run = $this->poster();
        $json_data = json_decode($first_run, true);
                
        foreach ($json_data['rooms'][$this->category] as $room)
        {
            $room_name = $room['name'];
            if (!array_key_exists($room_name, $this->rooms)) {
                $this->rooms[$room_name] = new Room($room);
            }
            else {
                $this->rooms[$room_name]->add_images($room['images']);
                $this->rooms[$room_name]->update_stats($room['users']);
            }
            
            $this->total_dir_users += $this->rooms[$room_name]->total_users;
        }
        $this->page_crawler();
    }
    
}
