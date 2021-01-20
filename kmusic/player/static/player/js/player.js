document.addEventListener('DOMContentLoaded', function(){
    controls_section = document.querySelector('#controls-section');
    time_left = parseFloat(controls_section.dataset.timeleft);

    pause_btn = document.querySelector('#pause_btn');
    console.log(time_left);
    if (time_left>0){
       setTimeout(refresh, time_left); 
    }
    
});

function refresh(){
    pause_btn = document.querySelector('#pause_btn');
    if(pause_btn!=null){
        console.log("song end");
        location.reload();
    }

}

