function showSection(sectionId, btn){

    // REMOVE ACTIVE
    document.querySelectorAll(".rooms-section")
    .forEach(section=>{
        section.classList.remove("active");
    });

    document.querySelectorAll(".tab-btn")
    .forEach(button=>{
        button.classList.remove("active");
    });

    // ADD ACTIVE
    document.getElementById(sectionId)
    .classList.add("active");

    btn.classList.add("active");
}


/* =========================
   UPDATE ROOM STATUS
========================= */

function updateRoomStatus(
    roomId,
    status,
    hostelType
){

    fetch("/dashboard/update-room-status/",{

        method: "POST",

        headers:{
            "Content-Type":"application/json"
        },

        body: JSON.stringify({

            room_id: roomId,
            status: status,
            hostel_type: hostelType

        })

    })

    .then(res => res.json())

    .then(data => {

        if(data.success){

            location.reload();

        }else{

            alert("Update failed");

        }

    });

}