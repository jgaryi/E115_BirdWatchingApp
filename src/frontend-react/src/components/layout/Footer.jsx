'use client'
import { usePathname } from 'next/navigation';

import styles from './Footer.module.css';

export default function Footer() {

    const pathname = usePathname();
    const hideFooter = pathname === '/chat';

    if (hideFooter) {
        return (
            <></>
        )
    } else {
        return (
            <footer className={styles.footer}>
                <p>The Bird Watching App {new Date().getFullYear()}</p>
            </footer>
        );
    }

}