(() => {
    const canvas = document.getElementById("confetti-canvas");

    if (!canvas) return;

    const context = canvas.getContext("2d");

    const reducedMotion = window.matchMedia(
        "(prefers-reduced-motion: reduce)"
    ).matches;

    if (reducedMotion) return;

    let particles = [];
    let animationFrame;

    const colors = [
        "#171717",
        "#555555",
        "#888888",
        "#bbbbbb",
        "#dedede"
    ];

    function resizeCanvas() {
        const ratio = Math.min(window.devicePixelRatio || 1, 2);

        canvas.width = window.innerWidth * ratio;
        canvas.height = window.innerHeight * ratio;

        context.setTransform(ratio, 0, 0, ratio, 0, 0);
    }

    function createParticles() {
        const amount = Math.min(
            Math.floor(window.innerWidth / 5),
            140
        );

        particles = [];

        for (let i = 0; i < amount; i++) {
            particles.push({
                x: Math.random() * window.innerWidth,
                y: -Math.random() * window.innerHeight,
                size: Math.random() * 7 + 3,
                speed: Math.random() * 3 + 2,
                rotation: Math.random() * 360,
                rotationSpeed: Math.random() * 8 - 4,
                horizontal: Math.random() * 2 - 1,
                color: colors[
                    Math.floor(Math.random() * colors.length)
                ],
                opacity: 1
            });
        }
    }

    function animate() {
        context.clearRect(
            0,
            0,
            window.innerWidth,
            window.innerHeight
        );

        particles.forEach((particle) => {
            particle.y += particle.speed;
            particle.x += particle.horizontal;
            particle.rotation += particle.rotationSpeed;

            if (particle.y > window.innerHeight) {
                particle.opacity -= 0.05;
            }

            context.save();

            context.globalAlpha = Math.max(0, particle.opacity);
            context.translate(particle.x, particle.y);
            context.rotate(particle.rotation * Math.PI / 180);

            context.fillStyle = particle.color;

            context.fillRect(
                -particle.size / 2,
                -particle.size / 2,
                particle.size,
                particle.size * 1.5
            );

            context.restore();
        });

        particles = particles.filter(
            particle => particle.opacity > 0
        );

        if (particles.length > 0) {
            animationFrame = requestAnimationFrame(animate);
        } else {
            context.clearRect(
                0,
                0,
                window.innerWidth,
                window.innerHeight
            );
        }
    }

    resizeCanvas();
    createParticles();
    animate();

    window.addEventListener("resize", resizeCanvas);

    window.addEventListener("pagehide", () => {
        cancelAnimationFrame(animationFrame);
        window.removeEventListener("resize", resizeCanvas);
    });
})();