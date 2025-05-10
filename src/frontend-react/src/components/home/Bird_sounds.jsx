
'use client';

import { useState, useEffect, useRef } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import styles from './Bird_sounds.module.css';
import Bird_soundCard from '../shared/Bird_soundCard';
import DataService from "../../services/DataService";


export default function bird_sounds() {
    // Component States
    const [episodes, setEpisodes] = useState([]);

    // Setup Component
    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await DataService.Getbird_sounds(4); // Limiting to 4 episodes for the main view
                setEpisodes(response.data);
            } catch (error) {
                console.error('Error fetching bird_sounds:', error);
                setEpisodes([]); // Set empty array in case of error
            }
        };

        fetchData();
    }, []);

    return (
        <section className={styles.section} id="bird_sounds">
            <h2 className={styles.title}>Bird Sounds Explorer</h2>
            <div className={styles.underline}></div>

            <div className={styles.content}>
                <div className={styles.aboutbird_sound} style={{ marginTop: '40px' }}>

                    <h3>About Bird Sounds Explorer</h3>
                    <p>
                        Welcome to the Bird Sounds Explorer, where we celebrate the incredible diversity of birds 
                        through their unique calls! 
                    </p>
                    <p>                        
                        Each bird call offers a glimpse into the vibrant ecosystems 
                        of the Yanachaga Chemillén National Park. 
                    </p> 
                    <p>   
                        Join us as we explore the natural symphony of the forest—one bird at a time.
                    </p>
                </div>

                <div className={styles.episodesList}>
                    {episodes[3] && (
                        <Bird_soundCard key={episodes[3].id} bird_sound={episodes[3]} />
                    )}
                </div>

            </div>
            <div className={styles.viewAllContainer}>
                <Link href="/bird_sounds" className={styles.viewAllButton}>
                    Access Bird Sounds Explorer
                </Link>
            </div>
        </section>
    )
}