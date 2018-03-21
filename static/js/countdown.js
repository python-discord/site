"use strict";

(function(){  // Use a closure to avoid polluting global scope
    const startjam = new Date(Date.UTC(2018, 2, 23));
    const endjam = new Date(Date.UTC(2018, 2, 26));

    let now = Date.now();
    let goal;

    if (now+1000 < endjam.getTime()) {  // Only do anything if the jam hasn't ended
        UIkit.notification(  // Spawn the notification
            {
                message:
                "<div class='uk-text-center'>" +
                "    <span id=\"countdown-title\" class=\"uk-text-center\">" +
                "        <a href=\"/info/jams\">Code Jam</a> Countdown" +
                "    </span>" +
                "    <p class='uk-text-large' id=\"countdown-remaining\"></p>" +
                "</div>",
                pos: "bottom-right",
                timeout: endjam - now
            }
        );

        const heading = document.getElementById("countdown-title");

        if (now > startjam.getTime()) {  // Jam's already started
            heading.innerHTML = "<a href=\"/info/jams\">code jam</a> Countdown ends in...";
            goal = endjam.getTime();
        } else {
            heading.innerHTML = "Next <a href=\"/info/jams\">code jam</a> starts in...";
            goal = startjam.getTime();
        }

        let refreshCountdown = setInterval(function() {  // Create a repeating task
            let delta = goal - Date.now();  // Time until the goal is met

            if (delta <= 1000) {  // Goal has been met, best reload
                clearInterval(refreshCountdown);
                return location.reload();
            }

            let days = Math.floor(delta / (24*60*60*1000));
            delta -= days * (24*60*60*1000);

            let hours = Math.floor(delta / (60*60*1000));
            delta -= hours * (60*60*1000);

            let minutes = Math.floor(delta / (60*1000));
            delta -= minutes * (60*1000);

            let seconds = Math.floor(delta / 1000);

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

            try {
                document.getElementById('countdown-remaining').innerHTML = `${days}:${hours}:${minutes}:${seconds}`;
            } catch (e) {  // Notification was probably closed, so we can stop counting
                return clearInterval(refreshCountdown);
            }
        }, 500);
    }
}());
