"use strict";

var currentSongID = null;
var progress_interval = null;
document.addEventListener('DOMContentLoaded', function () {
  song_info = document.querySelector('#song-info');
  currentSongID = song_info.dataset.songid;
  controls_section = document.querySelector('#controls-section'); //all changes interval

  setInterval(checkChanges, 5000); //pause button

  pause_btn = document.querySelector('#pause_btn');
  pause_btn.onclick = pausePlayback;

  if (pause_btn != null) {
    //progress bar interval
    progress_interval = setInterval(increaseProgressBar, 100, 100);
  }
});

function checkChanges() {
  var request = new XMLHttpRequest();
  request.open('GET', "getCurrentSongID");

  request.onload = function () {
    var response = request.responseText;
    var data = JSON.parse(request.responseText);
    console.log(data);

    if (currentSongID != data.song_id) {
      //song changed
      getCurrentSongInfo();
    } else {
      updateProgressBar(parseFloat(data.song_progress));
    }
  };

  request.send();
}

function updateProgressBar(progress) {
  progress_div = document.querySelector('#song-progress');
  percentage = 100 * (progress / parseFloat(progress_div.dataset.songduration));
  progress_div.style.width = percentage + "%";
  progress_div.setAttribute("data-songprogress", progress);
}

function increaseProgressBar(increase) {
  progress_div = document.querySelector('#song-progress');
  progress = parseFloat(progress_div.dataset.songprogress) + increase;
  percentage = 100 * (progress / parseFloat(progress_div.dataset.songduration));
  progress_div.style.width = percentage + "%";
  progress_div.setAttribute("data-songprogress", progress);
}

function refresh() {
  pause_btn = document.querySelector('#pause_btn');

  if (pause_btn != null) {
    console.log("song end"); //location.reload();

    getCurrentSongInfo();
  }
}

function getCurrentSongInfo() {
  var request = new XMLHttpRequest();
  request.open('GET', "getCurrentSongInfo_HTTP_RES");

  request.onload = function () {
    var response = request.responseText;
    var data = JSON.parse(request.responseText);
    console.log(data);

    if (currentSongID != data.song_id) {
      //song changed
      document.querySelector('#current-album').src = data.song_art;
      document.querySelector('#song-title').innerHTML = data.song_title;
      document.querySelector('#song-artist').innerHTML = data.song_artist;
      document.querySelector('#band-background').style.backgroundImage = "url('" + data.artist_image + "')";
      currentSongID = data.song_id;
      document.querySelector('#song-info').setAttribute("data-songid", currentSongID); //mini albums

      var album_counter = 0;
      document.querySelectorAll('.mini-album').forEach(function (element) {
        element.src = data.recents[album_counter];
        album_counter++;
      });
    }
  };

  request.send();
}

function pausePlayback() {
  var request = new XMLHttpRequest();
  request.open('GET', "pause");

  request.onload = function () {
    var response = request.responseText;
    var data = JSON.parse(request.responseText);
    console.log(data);

    if (data == 204) {
      clearInterval(progress_interval);
      pause_btn = document.querySelector('#pause_btn');
      pause_btn.onclick = resumePlayback;
      pause_btn.innerHTML = '<i class="material-icons">play_arrow</i>';
    }
  };

  request.send();
  return false;
}

function resumePlayback() {
  var request = new XMLHttpRequest();
  request.open('GET', "play");

  request.onload = function () {
    var response = request.responseText;
    var data = JSON.parse(request.responseText);
    console.log(data);

    if (data == 204) {
      progress_interval = setInterval(increaseProgressBar, 100, 100);
      pause_btn = document.querySelector('#pause_btn');
      pause_btn.onclick = pausePlayback;
      pause_btn.innerHTML = '<i class="material-icons">pause</i>';
    }
  };

  request.send();
  return false;
}