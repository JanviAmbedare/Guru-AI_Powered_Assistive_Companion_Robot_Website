const DB_NAME = "guru_registration";

const DB_VERSION = 1;

const FACE_STORE = "faces";

const VOICE_STORE = "voices";


function openDB() {

    return new Promise(
        (resolve, reject) => {

            const request =
                indexedDB.open(
                    DB_NAME,
                    DB_VERSION
                );

            request.onupgradeneeded =
                function(event) {

                    const db =
                        event.target.result;

                    if (
                        !db.objectStoreNames.contains(
                            FACE_STORE
                        )
                    ) {

                        db.createObjectStore(
                            FACE_STORE,
                            {
                                autoIncrement: true
                            }
                        );
                    }

                    if (
                        !db.objectStoreNames.contains(
                            VOICE_STORE
                        )
                    ) {

                        db.createObjectStore(
                            VOICE_STORE,
                            {
                                autoIncrement: true
                            }
                        );
                    }
                };

            request.onsuccess =
                () => resolve(
                    request.result
                );

            request.onerror =
                () => reject(
                    request.error
                );
        }
    );
}


async function saveFace(blob) {

    const db = await openDB();

    const tx =
        db.transaction(
            FACE_STORE,
            "readwrite"
        );

    tx.objectStore(
        FACE_STORE
    ).add(blob);
}


async function saveVoice(blob) {

    const db = await openDB();

    const tx =
        db.transaction(
            VOICE_STORE,
            "readwrite"
        );

    tx.objectStore(
        VOICE_STORE
    ).add(blob);
}


async function getFaces() {

    const db = await openDB();

    return new Promise(
        (resolve) => {

            const tx =
                db.transaction(
                    FACE_STORE,
                    "readonly"
                );

            const req =
                tx.objectStore(
                    FACE_STORE
                ).getAll();

            req.onsuccess =
                () => resolve(
                    req.result
                );
        }
    );
}


async function getVoices() {

    const db = await openDB();

    return new Promise(
        (resolve) => {

            const tx =
                db.transaction(
                    VOICE_STORE,
                    "readonly"
                );

            const req =
                tx.objectStore(
                    VOICE_STORE
                ).getAll();

            req.onsuccess =
                () => resolve(
                    req.result
                );
        }
    );
}


async function clearMedia() {

    const db = await openDB();

    db.transaction(
        FACE_STORE,
        "readwrite"
    )
    .objectStore(
        FACE_STORE
    )
    .clear();

    db.transaction(
        VOICE_STORE,
        "readwrite"
    )
    .objectStore(
        VOICE_STORE
    )
    .clear();
}