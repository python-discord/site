var heading = document.getElementById("countdown-title");
var startjam = new Date(Date.UTC(2018, 2, 23));
var endjam = new Date(Date.UTC(2018, 2, 26));
var goal;
var now = Date.now();
if (now+1000 >= endjam.getTime()) {
    heading.innerHTML = "Code Jam has finished!";
} else {
    if (now > startjam.getTime()) {
        heading.innerHTML = "Code Jam ends in...";
        goal = endjam.getTime();
    } else {
        heading.innerHTML = "Next Code Jam starts in...";
        goal = startjam.getTime();
    }
    var refreshCountdown = setInterval(function() {
        var delta = goal - Date.now();
        if (delta <= 1000) {
            clearInterval(refreshCountdown);
            location.reload();
        }
        var days = Math.floor(delta / (24*60*60*1000));
        delta -= days * (24*60*60*1000);
        var hours = Math.floor(delta / (60*60*1000));
        delta -= hours * (60*60*1000);
        var minutes = Math.floor(delta / (60*1000));
        delta -= minutes * (60*1000);
        var seconds = Math.floor(delta / 1000);
        if (days < 10) {
            days = "0"+days;
        }
        if (hours < 10) {
            hours = "0"+hours;
        }
        if (minutes < 10) {
            minutes = "0"+minutes;
        }
        if (seconds < 10) {
            seconds = "0"+seconds;
        }
        let formatted = `${days}:${hours}:${minutes}:${seconds}`
        document.getElementById('remaining').innerHTML = formatted;
    }, 100);
}
