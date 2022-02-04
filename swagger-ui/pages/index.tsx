import type { NextPage } from 'next'
import Head from 'next/head'
import Image from 'next/image'
import styles from '../styles/Home.module.css'
import { RedocStandalone } from 'redoc'

const Home: NextPage = () => {
  return (
    <div className={styles.container}>
      <Head>
        <title>API Doc of online-bot-test-backend</title>
        <meta name="description" content="hello" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className={styles.main}>
        <RedocStandalone
          specUrl='/openapi.json'
          options={{
            nativeScrollbars: true,
            theme: { colors: { primary: { main: '#dd5522' } } },
          }}
        />
      </main>

      <footer className={styles.footer}>
        <a
          href="https://vercel.com?utm_source=create-next-app&utm_medium=default-template&utm_campaign=create-next-app"
          target="_blank"
          rel="noopener noreferrer"
        >
          Powered by{' '}
          <span className={styles.logo}>
            <Image src="/vercel.svg" alt="Vercel Logo" width={72} height={16} />
          </span>
        </a>
      </footer>
    </div>
  )
}

export default Home
