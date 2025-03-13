document.addEventListener("DOMContentLoaded", () => {
    const formPrenotazione = document.getElementById("prenotazioneForm");
    const formFiltroEmail = document.getElementById("emailFilterForm");
    const cercaPrenotazioneButton = document.getElementById("cercaPrenotazione");
    const formModifica = document.getElementById("modificaForm");
    document.getElementById("cancellaPrenotazioneButton")?.addEventListener("click", cancellaPrenotazione);

    async function inviaPrenotazioneRequest(event, method = "POST", url = "http://127.0.0.1:8000/prenotazioni/") {
        event.preventDefault();

        const dataInput = document.getElementById("data").value;
        const formattedDate = new Date(dataInput).toISOString().split("T")[0]; // ✅ Converte in "YYYY-MM-DD"
    
        const data = {
            nome: document.getElementById("nome").value.trim(),
            cognome: document.getElementById("cognome").value.trim(),
            email: document.getElementById("email").value.trim(),
            telefono: document.getElementById("telefono").value.trim(),
            numero_persone: parseInt(document.getElementById("numero_persone").value, 10) || 1,
            data: formattedDate,
            ora_arrivo: document.getElementById("ora_arrivo").value || "12:00"
        };
    
        try {
            const response = await fetch(url, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                mode: "cors",
                body: JSON.stringify(data)
            });

            let result;
            try {
                result = await response.json(); // Gestisce il caso in cui il server non restituisca JSON valido
            } catch (jsonError) {
                throw new Error(`Risposta non valida dal server (${response.status})`);
            }
    
            if (!response.ok) {
                throw new Error(`Errore ${response.status}: ${JSON.stringify(result)}`);
            }
    
            alert(result.message || "Prenotazione effettuata con successo!");
        } catch (error) {
            console.error("Errore nella richiesta:", error);
            alert("Errore nella comunicazione con il server.");
        }
    }
    
    async function getPrenotazioneByEmail(email) {
        try {
            const response = await fetch(`http://127.0.0.1:8000/prenotazioni/email/?email=${email}`);
            if (!response.ok) throw new Error("Prenotazione non trovata");

            const data = await response.json();
            console.log("Prenotazione trovata:", data);
            
            document.getElementById("prenotazione-trovata").style.display = "block";
            document.getElementById("modifica_nome").value = data.nome;
            document.getElementById("modifica_cognome").value = data.cognome;
            document.getElementById("modifica_telefono").value = data.telefono;
            document.getElementById("modifica_numero_persone").value = data.numero_persone;
            document.getElementById("modifica_data").value = data.data.split("T")[0];
            document.getElementById("modifica_ora_arrivo").value = data.ora_arrivo;
            document.getElementById("modifica_email").value = data.email;
        } catch (error) {
            console.error("Errore:", error);
            alert("Prenotazione non trovata o errore nella comunicazione con il server.");
            document.getElementById("prenotazione-trovata").style.display = "none";
        }
    }

    async function aggiornaPrenotazione(event) {
        event.preventDefault(); // Evita il ricaricamento della pagina

        const email = document.getElementById("modifica_email")?.value; // Prendi l'email per identificare la prenotazione

        if (!email) {
            alert("Errore: Nessuna email trovata.");
            return;
        }

        const prenotazioneData = {
            nome: document.getElementById("modifica_nome")?.value.trim(),
            cognome: document.getElementById("modifica_cognome")?.value.trim(),
            telefono: document.getElementById("modifica_telefono")?.value.trim(),
            numero_persone: parseInt(document.getElementById("modifica_numero_persone")?.value, 10) || 1,
            data: document.getElementById("modifica_data")?.value,
            ora_arrivo: document.getElementById("modifica_ora_arrivo")?.value,
        };

        console.log("Dati inviati:", JSON.stringify(prenotazioneData));

        try {
            const response = await fetch(`http://127.0.0.1:8000/prenotazioni/${email}/`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(prenotazioneData),
            });

            if (!response.ok) {
                throw new Error(`Errore durante l'aggiornamento della prenotazione (${response.status})`);
            }

            alert("Prenotazione aggiornata con successo!");
        } catch (error) {
            console.error("Errore:", error);
            alert("Errore nella modifica della prenotazione.");
        }
    }

    // ✅ Aggiungi Event Listeners
    formPrenotazione?.addEventListener("submit", async (event) => {
        await inviaPrenotazioneRequest(event, "POST");
    });

    formFiltroEmail?.addEventListener("submit", async (event) => {
        event.preventDefault();
        const email = document.getElementById("emailFilter")?.value;
        if (email) {
            await getPrenotazioneByEmail(email);
        } else {
            alert("Inserisci un'email valida!");
        }
    });

    cercaPrenotazioneButton?.addEventListener("click", async (event) => {
        event.preventDefault();
        const email = document.getElementById("emailFilter")?.value;
        if (email) {
            await getPrenotazioneByEmail(email);
        } else {
            alert("Inserisci un'email valida!");
        }
    });

    formModifica?.addEventListener("submit", aggiornaPrenotazione);
});

// ✅ Funzione per lo slider delle immagini nel menù
const images = document.querySelectorAll(".menu-gallery img");
let index = 0;

function changeImage() {
    images[index].classList.remove("active");
    index = (index + 1) % images.length;
    images[index].classList.add("active");
}

setInterval(changeImage, 5000);

async function cancellaPrenotazione(event) {
    event.preventDefault(); // Evita il ricaricamento della pagina

    const email = document.getElementById("modifica_email")?.value; // Prendi l'email per identificare la prenotazione

    if (!email) {
        alert("Errore: Nessuna email trovata.");
        return;
    }

    if (!confirm("Sei sicuro di voler cancellare la prenotazione?")) {
        return;
    }

    try {
        const response = await fetch(`http://127.0.0.1:8000/prenotazioni/${email}/`, {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json",
            },
        });

        if (!response.ok) {
            throw new Error(`Errore durante la cancellazione della prenotazione (${response.status})`);
        }

        alert("Prenotazione cancellata con successo!");
        document.getElementById("prenotazione-trovata").style.display = "none"; // Nasconde la sezione di modifica
    } catch (error) {
        console.error("Errore:", error);
        alert("Errore nella cancellazione della prenotazione.");
    }
}
