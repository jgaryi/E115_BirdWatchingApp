import Link from 'next/link';
import styles from './About.module.css';

export default function About() {
    return (
        <section className={styles.about} id="about">
            <h1 className={styles.title}>About Us</h1>
            <div className={styles.underline}></div>
            <div className={styles.content}>
                <p>
                    <strong>Welcome to the Bird Watching App</strong>, a web application inspired by a shared passion 
                    for nature and cutting-edge technology. This site was created as a demonstration project to showcase 
                    the use of artificial intelligence in app development. 
                </p>
                <p>
                    We are Jaqueline Garcia-Yi, Susan Urban, Yong Li, and Victoria Okereke, Master's Students of E-115, 
                    a course at Harvard Extension School.
                </p>
                <p>
                    This app was developed in response to a request from leaders of the <strong>Ashaninka and Yanesha (also known as Amuesha)</strong> communities, 
                    who live within <strong>Yanachaga Chemillén National Park in Peru</strong>. These indigenous communities sought a tool to promote birdwatching 
                    and sustainable tourism within their ancestral territories.
                </p>
                <p>
                    The app currently highlights a selection of representative or vulnerable bird species experiencing population decline, all found within the national park, 
                    which is home to nearly <strong>500 bird species</strong>. 
                </p>
                <p>
                    Please note that this is a demonstration project, and some features may still be under development. 
                    We hope you enjoy exploring it and would love to hear your feedback. <strong>Feel free to send us your thoughts by email!</strong>
                </p>
                <p>
                    Thank you for visiting <strong>Bird Watching App</strong>, and we hope you have fun discovering the intersection of birds and
                    AI!
                </p>

                <Link href="mailto:jgarciayi@g.harvard.edu?subject=Feedback%20from%20BirdWatchingApp" className={styles.contactButton}>
                    CONTACT US
                </Link>
            </div>
        </section>
    );
}