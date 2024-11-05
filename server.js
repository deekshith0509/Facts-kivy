const express = require('express');
const cors = require('cors');
const app = express();
const port = 3000;

// Enable CORS for all routes
app.use(cors());

// Sample facts data
const facts = {
    random: [
        { fact: "Around 70% of people say that cooking at home makes them feel healthier and happier.", category: "General" },
        { fact: "Studies show that 65% of people feel more productive when they take short breaks during work or study.", category: "General" },
        { fact: "Approximately 80% of students find that collaborating with peers helps them understand their studies better.", category: "General" },
        { fact: "About 60% of people who practice gratitude regularly report feeling more positive about their lives.", category: "General" },
        { fact: "Nearly 75% of families say that spending time together strengthens their bonds and improves their happiness.", category: "General" },
        { fact: "Studies indicate that around 90% of people believe volunteering makes a positive impact on their communities.", category: "General" },
        { fact: "Over 70% of people feel more motivated to achieve their goals when they share them with friends or family.", category: "General" },
        { fact: "Around 80% of individuals who exercise regularly report having better mental health and well-being.", category: "General" },
        { fact: "Research shows that nearly 65% of adults find that reading helps them relax and escape daily stress.", category: "General" },
        { fact: "About 85% of people feel accomplished when they complete their daily to-do lists, boosting their motivation for the next day.", category: "General" },
        { fact: "Surveys show that nearly 75% of students believe that participating in extracurricular activities enhances their skills.", category: "General" },
        { fact: "Approximately 60% of parents say that spending time outdoors with their kids helps foster creativity and exploration.", category: "General" },
        { fact: "Around 70% of people feel that having a pet brings them joy and companionship, improving their overall happiness.", category: "General" },
        { fact: "Research indicates that 65% of people who practice mindfulness report reduced stress and increased focus.", category: "General" },
        { fact: "Over 80% of people find that listening to music improves their mood and helps them concentrate better.", category: "General" },
        { fact: "About 75% of individuals who set realistic goals say they achieve them, leading to greater satisfaction in life.", category: "General" }
    ],
    tech: [
        { fact: "Around 80% of students believe that technology helps them learn more effectively and engage with their studies.", category: "Tech" },
        { fact: "Studies show that using productivity apps can increase task completion rates by up to 40%.", category: "Tech" },
        { fact: "Approximately 70% of employees feel more connected to their teams when using collaborative online tools.", category: "Tech" },
        { fact: "Research indicates that 60% of families use smart home devices to save energy and improve convenience.", category: "Tech" },
        { fact: "Over 50% of online learners report that flexible learning platforms allow them to balance their studies with work and family.", category: "Tech" },
        { fact: "Around 75% of parents find that educational apps make learning fun for their children.", category: "Tech" },
        { fact: "Approximately 65% of people say that technology has improved their communication with friends and family.", category: "Tech" },
        { fact: "Studies show that 80% of users feel more secure when using password managers to protect their online accounts.", category: "Tech" },
        { fact: "Around 70% of people believe that social media has helped them reconnect with old friends and maintain relationships.", category: "Tech" },
        { fact: "Research indicates that 90% of employees feel more productive when using modern workplace technology.", category: "Tech" },
        { fact: "Nearly 80% of students say that online resources help them grasp difficult concepts better than traditional methods.", category: "Tech" },
        { fact: "Approximately 65% of people enjoy using virtual fitness classes to stay active from the comfort of their homes.", category: "Tech" },
        { fact: "About 75% of individuals feel that technology enhances their creativity and allows for self-expression.", category: "Tech" },
        { fact: "Studies show that 85% of people appreciate the convenience of online shopping, especially during busy times.", category: "Tech" },
        { fact: "Around 70% of parents believe that educational games on tablets help their children learn while having fun.", category: "Tech" },
        { fact: "Research indicates that 60% of professionals feel more confident in their skills after taking online courses.", category: "Tech" }
    ]
};

// Route to get a random fact
app.get('/random', (req, res) => {
    const randomFact = facts.random[Math.floor(Math.random() * facts.random.length)];
    res.json(randomFact);
});

// Route to get a tech fact
app.get('/tech', (req, res) => {
    const techFact = facts.tech[Math.floor(Math.random() * facts.tech.length)];
    res.json(techFact);
});

// Error handling middleware
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({ error: 'Something went wrong!' });
});

// Start the server
app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});