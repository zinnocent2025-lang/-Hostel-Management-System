const uploadBtn = document.getElementById("uploadBtn");
const fileInput = document.getElementById("fileInput");
const fileTableBody = document.getElementById("fileTableBody");
const foldersGrid = document.getElementById("foldersGrid");
const previewBox = document.getElementById("previewBox");
const searchInput = document.getElementById("searchInput");
const sortSelect = document.getElementById("sortSelect");


/* =========================
DELETE MODAL VARIABLES
========================= */

let deleteFileId = null;

const deleteModal =
    document.getElementById("deleteModal");

const deleteMessage =
    document.getElementById("deleteMessage");

const cancelDelete =
    document.getElementById("cancelDelete");

const confirmDelete =
    document.getElementById("confirmDelete");

/* =========================
MOBILE PREVIEW
========================= */

const mobilePreviewModal =
    document.getElementById("mobilePreviewModal");

const mobilePreviewBox =
    document.getElementById("mobilePreviewBox");

const closePreview =
    document.getElementById("closePreview");

/* =========================
DATA
========================= */

let filesData = [];

/* =========================
UPLOAD
========================= */

uploadBtn.addEventListener("click", () => {
    fileInput.click();
});

fileInput.addEventListener("change", async () => {

    const file = fileInput.files[0];

    if (!file) return;

    const formData = new FormData();

    formData.append("file", file);

    const folderSelect =
        document.getElementById("folderSelect");

    if (folderSelect) {
        formData.append(
            "folder_id",
            currentFolderId || folderSelect.value
        );
    }

    try {

        const response = await fetch(
            "/dashboard/upload-file/",
            {
                method: "POST",

                body: formData,

                headers: {
                    "X-CSRFToken": getCSRFToken()
                }
            }
        );

        const data = await response.json();

        console.log(data);

        if (data.success) {

            loadFiles();

            fileInput.value = "";

            alert("File uploaded successfully");

        } else {

            alert("Upload failed");
        }

    } catch (error) {

        console.error(error);

    }

});
/* =========================
LOAD FILES
========================= */

function loadFiles(folderId = '', folderName = 'All Files') {

    let url = '/dashboard/get-files/';

    currentFolderId = folderId;

    currentFolderName = folderName;

    folderPath.innerText = folderName;

    if (folderId) {

        url += `?folder=${folderId}`;
    }

    fetch(url)
        .then(response => response.json())
        .then(data => {

            console.log(data);

            filesData = data.files;
            renderFiles(data.files);

        });
}

const folderPath = document.getElementById("folderPath");
const folderSelect =  document.getElementById("folderSelect");

let currentFolderId = null;

let currentFolderName = "All Files";

folderPath.addEventListener("click", () => {

    loadFiles();

});

/* =========================
SELECT FOLDER DROPDOWN
========================= */

folderSelect.addEventListener("change", () => {

    const folderId = folderSelect.value;

    if (!folderId) {

        loadFiles();

        return;
    }

    const selectedOption =
        folderSelect.options[
            folderSelect.selectedIndex
        ];

    const folderName =
        selectedOption.text;

    loadFiles(
        folderId,
        folderName
    );

});
/* =========================
RENDER FILES
========================= */

function renderFiles(files) {
    console.log(files);

    fileTableBody.innerHTML = "";

    if (files.length === 0) {

        fileTableBody.innerHTML = `
        <tr>
            <td colspan="5"
                style="
                    text-align:center;
                    padding:40px;
                    color:gray;
                ">
                Folder is empty
            </td>
        </tr>
    `;

        return;
    }

    files.forEach(file => {

        const row = document.createElement("tr");

        row.classList.add("file-row");

        row.innerHTML = `

    <td class="file-name">
        ${file.name}
    </td>

    <td>
        ${file.type}
    </td>

    <td>
        ${file.size}
    </td>

    <td>
        ${file.uploaded_at}
    </td>

    <td>

        <div class="file-actions">

            <button
                class="rename-btn"
                onclick="event.stopPropagation();
                renameFile(${file.id}, '${file.name}')">

                Rename
            </button>

            <button
                class="action-btn"
                onclick="event.stopPropagation();
                deleteFile(${file.id}, '${file.name}')">

                Delete
            </button>

        </div>

    </td>

`;
        row.addEventListener("click", () => {
            previewFile(file);
        });

        fileTableBody.appendChild(row);
    });
}

/* =========================
PREVIEW FILE
========================= */

function previewFile(file) {

    const ext =
        file.name.split(".").pop().toLowerCase();

    /* IMAGE */

    if (["jpg", "jpeg", "png", "gif", "webp"].includes(ext)) {

        previewBox.innerHTML = `
            <img src="${file.url}">

            <div class="file-info">

                <p>
                    <strong>Name:</strong> ${file.name}
                </p>

                <p>
                    <strong>Type:</strong> Image
                </p>

            </div>

            <div class="preview-actions">

                <button onclick="window.open('${file.url}')">
                    Open
                </button>

            </div>
        `;
    }

    /* VIDEO */

    else if (["mp4", "webm", "ogg"].includes(ext)) {

        previewBox.innerHTML = `
            <video controls>

                <source src="${file.url}">

            </video>

            <div class="file-info">

                <p>
                    <strong>Name:</strong> ${file.name}
                </p>

                <p>
                    <strong>Type:</strong> Video
                </p>

            </div>

            <div class="preview-actions">

                <button onclick="window.open('${file.url}')">
                    Open
                </button>

            </div>
        `;
    }

    /* PDF */

    else if (ext === "pdf") {

        previewBox.innerHTML = `
            <iframe src="${file.url}"></iframe>

            <div class="file-info">

                <p>
                    <strong>Name:</strong> ${file.name}
                </p>

                <p>
                    <strong>Type:</strong> PDF
                </p>

            </div>

            <div class="preview-actions">

                <button onclick="window.open('${file.url}')">
                    Open PDF
                </button>

            </div>
        `;
    }

    /* WORD */

    else if (["doc", "docx"].includes(ext)) {

        previewBox.innerHTML = `
            <div class="file-info">

                <p>
                    <strong>Name:</strong> ${file.name}
                </p>

                <p>
                    <strong>Type:</strong> Word Document
                </p>

            </div>

            <div class="preview-actions">

                <button onclick="window.open('${file.url}')">
                    Open Document
                </button>

            </div>
        `;
    }

    /* OTHER FILES */

    else {

        previewBox.innerHTML = `
            <div class="file-info">

                <p>
                    <strong>Name:</strong> ${file.name}
                </p>

                <p>
                    Preview not available
                </p>

            </div>

            <div class="preview-actions">

                <button onclick="window.open('${file.url}')">
                    Open File
                </button>

            </div>
        `;
    }

    /* MOBILE PREVIEW */

    if (window.innerWidth <= 1100) {

        mobilePreviewBox.innerHTML =
            previewBox.innerHTML;

        mobilePreviewModal.classList.add("active");
    }
}

/* =========================
DELETE FILE MODAL
========================= */

function deleteFile(id, fileName) {

    deleteFileId = id;

    deleteMessage.innerHTML =
        `Are you sure you want to delete <strong>${fileName}</strong>?`;

    deleteModal.classList.add("active");
}

/* =========================
CONFIRM DELETE
========================= */

confirmDelete.addEventListener("click", async () => {

    if (!deleteFileId) return;

    const response = await fetch(
        `/dashboard/delete-file/${deleteFileId}/`,
        {
            method: "DELETE",

            headers: {
                "X-CSRFToken": getCSRFToken()
            }
        }
    );

    const data = await response.json();

    if (data.success) {

        loadFiles();

        previewBox.innerHTML =
            `<p>Select a file</p>`;
    }

    deleteModal.classList.remove("active");

    deleteFileId = null;
});

/* =========================
CANCEL DELETE
========================= */

cancelDelete.addEventListener("click", () => {

    deleteModal.classList.remove("active");

    deleteFileId = null;
});

/* =========================
SEARCH
========================= */

searchInput.addEventListener("input", () => {

    const value =
        searchInput.value.toLowerCase();

    const filtered =
        filesData.filter(file =>
            file.name.toLowerCase().includes(value)
        );

    renderFiles(filtered);
});

/* =========================
SORT
========================= */

sortSelect.addEventListener("change", () => {

    const value = sortSelect.value;

    if (value === "newest") {

        filesData.sort((a, b) =>
            new Date(b.uploaded_at) - new Date(a.modified)
        );
    }

    else {

        filesData.sort((a, b) =>
            new Date(a.uploaded_at) - new Date(b.modified)
        );
    }

    renderFiles(filesData);
});

/* =========================
CSRF TOKEN
========================= */

function getCSRFToken() {

    const cookies =
        document.cookie.split(";");

    for (let cookie of cookies) {

        cookie = cookie.trim();

        if (cookie.startsWith("csrftoken=")) {

            return cookie.substring(
                "csrftoken=".length
            );
        }
    }

    return "";
}

/* =========================
MOBILE SIDEBAR
========================= */

document.addEventListener("DOMContentLoaded", () => {

    const mobileMenuBtn =
        document.getElementById("mobileMenuBtn");

    const sidebar =
        document.getElementById("sidebar");

    const sidebarOverlay =
        document.getElementById("sidebarOverlay");

    if (mobileMenuBtn) {

        mobileMenuBtn.addEventListener("click", () => {

            sidebar.classList.add("active");

            sidebarOverlay.classList.add("active");
        });
    }

    if (sidebarOverlay) {

        sidebarOverlay.addEventListener("click", () => {

            sidebar.classList.remove("active");

            sidebarOverlay.classList.remove("active");
        });
    }

    if (sidebar) {

        sidebar.addEventListener("click", (e) => {

            e.stopPropagation();
        });
    }
});

/* =========================
CLOSE MOBILE PREVIEW
========================= */

if (closePreview) {

    closePreview.addEventListener("click", () => {

        mobilePreviewModal.classList.remove("active");
    });
}

/* =========================
START
========================= */

loadFiles();

document.querySelectorAll('.folder-item').forEach(folder => {

    folder.addEventListener('click', () => {

        const folderId =
            folder.dataset.folder;

        const folderName =
            folder.innerText.trim();

        loadFiles(
            folderId,
            folderName
        );

    });

});
/* =========================
CREATE FOLDER
========================= */

const newFolderBtn =
    document.getElementById("newFolderBtn");

const folderModal =
    document.getElementById("folderModal");

const cancelFolderBtn =
    document.getElementById("cancelFolderBtn");

const createFolderBtn =
    document.getElementById("createFolderBtn");

const folderNameInput =
    document.getElementById("folderNameInput");

if (newFolderBtn) {

    newFolderBtn.addEventListener("click", () => {

        folderModal.classList.add("active");

    });

}

if (cancelFolderBtn) {

    cancelFolderBtn.addEventListener("click", () => {

        folderModal.classList.remove("active");

    });

}

if (createFolderBtn) {

    createFolderBtn.addEventListener("click", async () => {

        const folderName =
            folderNameInput.value.trim();

        if (!folderName) return;

        const formData = new FormData();

        formData.append("name", folderName);

        const response = await fetch(
            "/dashboard/create-folder/",
            {
                method: "POST",

                body: formData,

                headers: {
                    "X-CSRFToken":
                        getCSRFToken()
                }
            }
        );

        const data =
            await response.json();

        if (data.success) {

            const folderList =
                document.querySelector(".folders-list");

            const div =
                document.createElement("div");

            div.classList.add("folder-item");

            div.dataset.folder = data.id;

            div.innerHTML = `
    <i class="fa-solid fa-folder"></i>

    <span>${data.name}</span>

    <div class="folder-actions">

        <button
            class="rename-folder-btn"
            onclick="event.stopPropagation();
            renameFolder(${data.id}, '${data.name}')">

            <i class="fa-solid fa-pen"></i>

        </button>

        <button
            class="delete-folder-btn"
            onclick="event.stopPropagation();
            deleteFolder(${data.id})">

            <i class="fa-solid fa-trash"></i>

        </button>

    </div>
`;

            folderList.appendChild(div);

            folderModal.classList.remove("active");

            folderNameInput.value = "";

        }

    });

}

/* =========================
FOLDER FILTER
========================= */

document.addEventListener("click", async (e) => {

    const folderItem =
        e.target.closest(".folder-item");

    if (!folderItem) return;

    document
        .querySelectorAll(".folder-item")
        .forEach(item => {

            item.classList.remove("active");

        });

    folderItem.classList.add("active");

    const folderId =
        folderItem.dataset.folder;

    const folderName =    folderItem.querySelector("span").innerText;

    folderPath.innerText = folderName;

    currentFolderId = folderId;

    const response =
        await fetch(
            `/dashboard/get-files/?folder=${folderId}`
        );

    const data =
        await response.json();

    filesData = data.files;

    renderFiles(data.files);

});

async function deleteFolder(folderId) {

    const confirmDelete =
        confirm("Delete this folder?");

    if (!confirmDelete) return;

    const response = await fetch(
        `/dashboard/delete-folder/${folderId}/`,
        {
            method: "DELETE",

            headers: {
                "X-CSRFToken": getCSRFToken()
            }
        }
    );

    const data = await response.json();

    if (data.success) {

        location.reload();

    }

}

async function renameFile(id, oldName) {

    const newName =
        prompt("Rename file:", oldName);

    if (!newName) return;

    const response = await fetch(
        `/dashboard/rename-file/${id}/`,
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken()
            },

            body: JSON.stringify({
                name: newName
            })
        }
    );

    const data = await response.json();

    if (data.success) {

        loadFiles(
            currentFolderId,
            currentFolderName
        );

    }

}

async function renameFolder(folderId, oldName) {

    const newName =
        prompt("Rename folder:", oldName);

    if (!newName) return;

    const response = await fetch(
        `/dashboard/rename-folder/${folderId}/`,
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken()
            },

            body: JSON.stringify({
                name: newName
            })
        }
    );

    const data = await response.json();

    if (data.success) {

        location.reload();

    }

}

/* =========================
SIDEBAR FILTERS
========================= */

document.querySelectorAll(".menu-item").forEach(item => {

    item.addEventListener("click", () => {

        document.querySelectorAll(".menu-item")
            .forEach(menu => menu.classList.remove("active"));

        item.classList.add("active");

        const type = item.dataset.type;

        if (type === "all") {

            renderFiles(filesData);

            return;
        }

        const filtered = filesData.filter(file => {

            const ext = file.type.toLowerCase();

            if (type === "image") {

                return ["jpg", "jpeg", "png", "gif", "webp"]
                    .includes(ext);
            }

            if (type === "pdf") {

                return ext === "pdf";
            }

            if (type === "document") {

                return ["doc", "docx", "txt"]
                    .includes(ext);
            }

            if (type === "video") {

                return ["mp4", "webm", "ogg"]
                    .includes(ext);
            }

        });

        renderFiles(filtered);

    });

});

/* =========================
SIDEBAR FILTERS
========================= */

document.querySelectorAll(".menu-item").forEach(item => {

    item.addEventListener("click", () => {

        document.querySelectorAll(".menu-item")
            .forEach(menu => menu.classList.remove("active"));

        item.classList.add("active");

        const type = item.dataset.type;

        if (type === "all") {

            renderFiles(filesData);

            return;
        }

        const filtered = filesData.filter(file => {

            const ext = file.type.toLowerCase();

            if (type === "image") {

                return ["jpg", "jpeg", "png", "gif", "webp"]
                    .includes(ext);
            }

            if (type === "pdf") {

                return ext === "pdf";
            }

            if (type === "document") {

                return ["doc", "docx", "txt"]
                    .includes(ext);
            }

            if (type === "video") {

                return ["mp4", "webm", "ogg"]
                    .includes(ext);
            }

        });

        renderFiles(filtered);

    });

});