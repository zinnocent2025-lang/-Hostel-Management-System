let currentVersion = null;

async function refreshRooms() {

    try {

        const response = await fetch(
            "/male-hostel/?partial=rooms&t=" + Date.now(),
            {
                cache: "no-store"
            }
        );

        if (!response.ok) return;

        const html = await response.text();

        const parser = new DOMParser();

        const doc = parser.parseFromString(html, "text/html");

        const newRooms = doc.querySelector(".room-container");

        const oldRooms = document.querySelector(".room-container");

        if (newRooms && oldRooms) {

            oldRooms.innerHTML = newRooms.innerHTML;

        }

    }

    catch(error){

        console.log(error);

    }

}

async function checkSystemUpdates() {

    try {

        const response = await fetch(
            "/system-version/?t=" + Date.now(),
            {
                cache:"no-store"
            }
        );

        if(!response.ok) return;

        const data = await response.json();

        if(currentVersion === null){

            currentVersion = data.version;

            return;

        }

        if(currentVersion !== data.version){

            currentVersion = data.version;

            console.log("Room data changed.");

            refreshRooms();

        }

    }

    catch(error){

        console.log(error);

    }

}

checkSystemUpdates();

setInterval(checkSystemUpdates,3000);