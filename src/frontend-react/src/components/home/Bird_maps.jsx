'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import styles from './Bird_maps.module.css';
import DataService from "../../services/DataService";


export default function bird_map() {
    // Component States
    const [bird_maps, setbird_maps] = useState([]);

    // Setup Component
    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await DataService.Getbird_maps(4); // Limiting to 4 episodes for the main view
                setbird_maps(response.data);
            } catch (error) {
                console.error('Error fetching bird_sounds:', error);
                setbird_maps([]); // Set empty array in case of error
            }
        };

        fetchData();
    }, []);

    return (
        <section className={styles.section} id="bird_maps">
            <h2 className={styles.title}>Interactive Maps</h2>
            <div className={styles.underline}></div>

            <div className={styles.content}>
                <div className={styles.bird_mapGrid}>
                    {bird_maps.map((bird_map) => (
                        <article key={bird_map.id} className={styles.bird_mapCard}>
                            <div className={styles.cardHeader}>
                                <span className={styles.date}>{bird_map.date}</span>
                                <span className={styles.readTime}>{bird_map.readTime}</span>
                            </div>

                            <h3 className={styles.bird_mapTitle}>{bird_map.title}</h3>

                            <p className={styles.excerpt}>{bird_map.excerpt}</p>

                            <Link href={`/bird_maps?id=${bird_map.id}`} className={styles.readMore}>
                                Discover More →
                            </Link>
                        </article>
                    ))}
                </div>
                <div className={styles.aboutbird_map}>
                    <div style={{ textAlign: 'right', marginTop: '50px' }}>
                        <Image
                            src="/assets/bird_map.png"
                            alt="bird_map Icon"
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
                <Link href="/bird_maps" className={styles.viewAllButton}>
                    View All Maps
                </Link>
            </div>
        </section>
    );
}