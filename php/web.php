<?php

function default_header()
{
    $header = array(
        'Accept: */*',
        'User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:59.0) Gecko/20100101 Firefox/59.0',
        'Accept-Encoding: deflate',
        'Accept-Language: en-US,en;q=0.5',
        'Connection: keep-alive'
    );
     
    return $header;
}

function curl_defaults()
{
    $options = array(
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_TIMEOUT => 20,
        CURLOPT_AUTOREFERER => true,
        CURLOPT_CAINFO => ''  // Set path to cacert.pem
    );
    
    return $options;
}

function get($url)
{
    $curl = curl_init($url);
    
    curl_setopt_array($curl, curl_defaults());
    curl_setopt($curl, CURLOPT_HTTPHEADER, default_header());
    
    $content = curl_exec($curl);
    $header = curl_getinfo($curl);
    $error = curl_error($curl);
    
    curl_close($curl);
    
    $response = array(
        'content' => $content,
        'header' => $header,
        'error' => $error
    );
    
    return $response;
}

function post($post_url, $post_data, $header=null)
{
    $curl = curl_init($post_url);
    curl_setopt_array($curl, curl_defaults());
    
    if ($header != null) {
        if (count($header) > 0) {
            curl_setopt($curl, CURLOPT_HTTPHEADER, $header);
        }
    }
    else {
        curl_setopt($curl, CURLOPT_HTTPHEADER, default_header());
    }
    
    curl_setopt($curl, CURLOPT_POST, 1);
    curl_setopt($curl, CURLOPT_POSTFIELDS, $post_data);
    
    $content = curl_exec($curl);
    $curl_info = curl_getinfo($curl);
    $error = curl_error($curl);
    
    curl_close($curl);

    $response = array(
        'content' => $content,
        'header' => $curl_info,
        'error' => $error
    );
    
    return $response;
}
