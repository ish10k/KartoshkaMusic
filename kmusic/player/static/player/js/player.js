document.addEventListener('DOMContentLoaded', function(){
    controls_section = document.querySelector('#controls-section');
    time_left = parseFloat(controls_section.dataset.timeleft);
    console.log(time_left);
    if (time_left>0){
       setTimeout(refresh, time_left); 
    }
    
});

function refresh(){
    console.log("song end");
    location.reload();
}

