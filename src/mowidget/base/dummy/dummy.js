function render({ model, el }) {
    let particles = [];

    const createParticles = () => {
        const container = document.createElement("div");
        container.className = "dummy-container";

        // Create bouncing text
        const text = document.createElement("div");
        text.className = "bouncing-text rainbow-text";
        text.textContent = model.get("message");
        container.appendChild(text);

        // Create floating particles
        const particleCount = model.get("particle_count");
        const emojis = ["✨", "🌟", "💫", "⭐", "🎈", "🎨", "🎭", "🎪"];

        for (let i = 0; i < particleCount; i++) {
            const particle = document.createElement("div");
            particle.className = "particle";
            particle.textContent =
                emojis[Math.floor(Math.random() * emojis.length)];
            particle.style.left = `${Math.random() * 100}%`;
            particle.style.top = `${Math.random() * 100}%`;
            particle.style.animationDuration = `${3 + Math.random() * 2}s`;
            particle.style.fontSize = `${12 + Math.random() * 12}px`;
            container.appendChild(particle);
            particles.push(particle);
        }

        el.innerHTML = "";
        el.appendChild(container);
    };

    createParticles();

    const handleMessageChange = () => {
        createParticles();
    };

    const handleParticleCountChange = () => {
        createParticles();
    };

    model.on("change:message", handleMessageChange);
    model.on("change:particle_count", handleParticleCountChange);

    // Cleanup function
    return () => {
        particles = [];
        el.innerHTML = "";
    };
}

export default { render };
