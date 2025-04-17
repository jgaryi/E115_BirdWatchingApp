'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import styles from './Newsletters.module.css';
//import DataService from "../../services/MockDataService"; // Mock
import DataService from "../../services/DataService";


export default function Newsletter() {
    // Component States
    const [newsletters, setNewsletters] = useState([]);

    // Setup Component
    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await DataService.GetNewsletters(4); // Limiting to 4 episodes for the main view
                setNewsletters(response.data);
            } catch (error) {
                console.error('Error fetching podcasts:', error);
                setNewsletters([]); // Set empty array in case of error
            }
        };

        fetchData();
    }, []);

    return (
        <section className={styles.section} id="newsletters">
            <h2 className={styles.title}>Interactive Maps</h2>
            <div className={styles.underline}></div>

            <div className={styles.content}>
                <div className={styles.newsletterGrid}>
                    {newsletters.map((newsletter) => (
                        <article key={newsletter.id} className={styles.newsletterCard}>
                            <div className={styles.cardHeader}>
                                <span className={styles.date}>{newsletter.date}</span>
                                <span className={styles.readTime}>{newsletter.readTime}</span>
                            </div>

                            <h3 className={styles.newsletterTitle}>{newsletter.title}</h3>

                            <p className={styles.excerpt}>{newsletter.excerpt}</p>

                            <Link href={`/newsletters?id=${newsletter.id}`} className={styles.readMore}>
                                Discover More →
                            </Link>
                        </article>
                    ))}
                </div>
                <div className={styles.aboutNewsletter}>
                    <div style={{ textAlign: 'right', marginTop: '50px' }}>
                        <Image
                            src="/assets/newsletter.png"
                            alt="Newsletter Icon"
                            width={400}
                            height={400}

                        />
                        <p className="text-sm text-black mt-2 mr-1">
                            Artwork by David Quinn
                        </p>
                    </div>

                    <h3>About Maps</h3>
                    <p>
                        Welcome to Bird Watching App's Maps! 
                    </p>
                    <p>
                        Explore the fascinating world of birds 
                        through our interactive maps, featuring previously identified bird locations within the Yanachaga Chemillén National Park. 
                    </p>
                    <p>
                        Discover habitat details and observe environmental changes over time that help explain why these species are vulnerable or endangered. 
                    </p>
                </div>
            </div>
            <div className={styles.viewAllContainer}>
                <Link href="/newsletters" className={styles.viewAllButton}>
                    View All Maps
                </Link>
            </div>
        </section>
    );
}