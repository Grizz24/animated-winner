const container = document.getElementById('container');

const headings = {
    surprise: 'The Oracle has spoken! Your pick is:',
    continue: 'Pick up where you left off:',
    new: 'Time to start something new:',
};

const emptyMessages = {
    surprise: 'Your list is empty. Add some shows first!',
    continue: "You aren't watching anything right now.",
    new: "You have nothing planned. Add something to 'Planning To'!",
};

const againLabels = {
    surprise: 'Find Another World',
    continue: 'Pick Another',
    new: 'Pick Another',
};

async function showPick(mode, excludeId) {
    let url = `${window.PICK_URL}?mode=${encodeURIComponent(mode)}`;
    if (excludeId) {
        url += `&exclude=${encodeURIComponent(excludeId)}`;
    }

    let data;
    try {
        const response = await fetch(url);
        data = await response.json();
    } catch (err) {
        container.replaceChildren(makeEl('h2', 'Something went wrong. Please try again.'));
        return;
    }

    if (!data.found) {
        container.replaceChildren(makeEl('h2', emptyMessages[mode]));
        return;
    }

    const details = [data.type, data.genre].filter(Boolean).join(' · ');
    const nextBtn = makeEl('button', againLabels[mode]);
    nextBtn.onclick = () => showPick(mode, data.id);

    // textContent (via makeEl) keeps show names from being treated as HTML.
    container.replaceChildren(
        makeEl('h2', headings[mode]),
        makeEl('h3', data.name),
        makeEl('p', details),
        nextBtn
    );
}

function makeEl(tag, text) {
    const el = document.createElement(tag);
    el.textContent = text;
    return el;
}

document.getElementById('surpriseBtn').onclick = () => showPick('surprise');
document.getElementById('continueBtn').onclick = () => showPick('continue');
document.getElementById('newBtn').onclick = () => showPick('new');
