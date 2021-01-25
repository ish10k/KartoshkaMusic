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
        location.reload();
    }

}

