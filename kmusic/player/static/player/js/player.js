document.addEventListener('DOMContentLoaded', function(){
    controls_section = document.querySelector('#controls-section');


    updateProgressBar();
    //pause button
    time_left = parseFloat(controls_section.dataset.timeleft);
    pause_btn = document.querySelector('#pause_btn');
    if (pause_btn!=null){
        //progress bar
        progress_interval = setInterval(updateProgressBar, 100);
    }

    if (time_left>0){
        refresh_timeout = setTimeout(refresh, time_left);
     }
    pause_btn.onclick = function(){
        clearTimeout(refresh_timeout);
        clearInterval(progress_interval);
    }
    console.log(time_left);

    //play button
    play_btn = document.querySelector('#play_btn');
    play_btn.onclick = function(){
        refresh_timeout = setTimeout(refresh, time_left);
        progress_interval = setInterval(updateProgressBar, 100);
    }

});

function updateProgressBar(){
    progress_div = document.querySelector('#song-progress');
    progress= parseFloat(progress_div.dataset.songprogress);
    percentage = 100*(progress/parseFloat(progress_div.dataset.songduration));
    //console.log(percentage+"%");
    progress_div.style.width=percentage+"%";
    progress_div.setAttribute("data-songprogress", progress+100);
}

function refresh(){
    pause_btn = document.querySelector('#pause_btn');
    if(pause_btn!=null){
        console.log("song end");
        //location.reload();
        getCurrentSongInfo();
    }

}

function getCurrentSongInfo(){
    const request = new XMLHttpRequest();
    request.open('GET', "getCurrentSongInfo_HTTP_RES");
    request.onload = () => {
        const response = request.responseText;
        const data = JSON.parse(request.responseText);
        console.log(data);

        document.querySelector('#current-album').src = data.song_art;
        document.querySelector('#song-title').innerHTML = data.song_title;
        document.querySelector('#song-artist').innerHTML = data.song_artist;
        document.querySelector('#band-background').style.backgroundImage = "url('"+data.artist_image+"')";

        //mini albums
        let album_counter = 0;
        document.querySelectorAll('.mini-album').forEach(function (element) {
            element.src = data.recents[album_counter];
            album_counter++;
        });
    
    };
    request.send();
}
