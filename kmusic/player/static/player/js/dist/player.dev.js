"use strict";

var currentSongID = null;
var progress_interval = null;
document.addEventListener('DOMContentLoaded', function () {
  song_info = document.querySelector('#song-info');
  currentSongID = song_info.dataset.songid;
  controls_section = document.querySelector('#controls-section'); //all changes interval

  setInterval(checkChanges, 5000); //pause button

  pause_btn = document.querySelector('#pause_btn');

  if (pause_btn != null) {
    pause_btn.onclick = pausePlayback; //progress bar interval

    progress_interval = setInterval(increaseProgressBar, 100, 100);
  } //play button


  play_btn = document.querySelector('#play_btn');

  if (play_btn != null) {
    play_btn.onclick = resumePlayback;
  } //skip previous button


  previous_btn = document.querySelector('#skip_previous');
  previous_btn.onclick = skip_previous; //skip next button

  next_btn = document.querySelector('#skip_next');
  next_btn.onclick = skip_next;
});

function skip_previous() {
  var request = new XMLHttpRequest();
  request.open('GET', "skip_previous");

  request.onload = function () {
    var response = request.responseText;
    var data = JSON.parse(request.responseText);
    console.log(data);
    clearInterval(progress_interval);
    getCurrentSongInfo();
  };

  request.send();
  return false;
}

function skip_next() {
  var request = new XMLHttpRequest();
  request.open('GET', "skip_next");

  request.onload = function () {
    var response = request.responseText;
    var data = JSON.parse(request.responseText);
    console.log(data);
    clearInterval(progress_interval);
    getCurrentSongInfo();
  };

  request.send();
  return false;
}

function checkChanges() {
  var request = new XMLHttpRequest();
  request.open('GET', "getCurrentSongID");

  request.onload = function () {
    var response = request.responseText;
    var data = JSON.parse(request.responseText); //console.log(data);

    if (currentSongID != data.song_id) {
      //song changed
      getCurrentSongInfo();
    } else {
      setProgressBar(parseFloat(data.song_progress));
    }
  };

  request.send();
}

function setProgressBar(progress) {
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
      document.querySelector('#song-info').setAttribute("data-songid", currentSongID);
      document.querySelector('#song-progress').setAttribute("data-songprogress", data.song_progress);
      document.querySelector('#song-progress').setAttribute("data-songduration", data.song_duration);
      setProgressBar(parseFloat(data.song_progress));
      progress_interval = setInterval(increaseProgressBar, 100, 100); //mini albums

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