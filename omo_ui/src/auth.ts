import NextAuth from "next-auth"
import Google from "next-auth/providers/google"
import { buildApiUrl } from "./utils/api"
import { Provider } from "next-auth/providers"
import { getCsrfToken } from "next-auth/react"

const providers: Provider[] = [
    Google({
        clientId: process.env.NEXT_PUBLIC_GOOGLE_CLOUD_CLIENT_ID as string,
        clientSecret: process.env.GOOGLE_CLOUD_CLIENT_SECRET as string,
    })
]

export const providerMap = providers.map((provider: any) => {
  if (typeof provider === "function") {
    const providerData = provider()
    return { id: providerData.id, name: providerData.name }
  } else {
    return { id: provider.id, name: provider.name }
  }
})
 
export const { handlers, signIn, signOut, auth } = NextAuth({
    providers: providers,
    pages: {
      signIn: "/login",
    },
    cookies: {
      sessionToken: { // we have to set custom domains for cookies
        name: process.env.APP_ENV === 'prod' ? '__Secure-authjs.session-token' : 'authjs.session-token', // keep the same name
        options: {
          httpOnly: true,
          sameSite: 'lax',
          path: '/',
          secure: true,
          domain: process.env.APP_ENV === 'prod' ? '.helloomo.ai' : undefined
        },
      },
      csrfToken: {
        name: process.env.APP_ENV === 'prod' ? '__Secure-authjs.csrf-token' : 'authjs.csrf-token', // keep the same name
        options: {
          httpOnly: true,
          sameSite: 'lax',
          path: '/',
          secure: true,
          domain: process.env.APP_ENV === 'prod' ? '.helloomo.ai' : undefined
        }, 
      },
      callbackUrl: {
        name: process.env.APP_ENV === 'prod' ? '__Secure-authjs.callback-url' : 'authjs.callback-url', // keep the same name
        options: {
          httpOnly: true,
          sameSite: 'lax',
          path: '/',
          secure: true,
          domain: process.env.APP_ENV === 'prod' ? '.helloomo.ai' : undefined
        },
      },
    },
    callbacks: {
        async redirect({ url, baseUrl}) {
            if (url.startsWith("/")) return `${baseUrl}/${url}`

            // Allows callback URLs on the same origin
            if (new URL(url).origin === baseUrl) return url

            return baseUrl
        },
        async jwt({ token, user, account, profile }) {
          // this callback is called after sign-in or page refresh

          if (profile) {
            const payload = {
              email: profile?.email,
              name: profile?.name,
              type: account?.type,
              provider: account?.provider,
              provider_account_id: account?.providerAccountId,
              refresh_token: account?.refresh_token,
              access_token: account?.access_token,
              expires_at: account?.expires_at,
              id_token: account?.id_token,
              scope: account?.scope,
              token_type: account?.token_type
            }
            const response = await fetch(buildApiUrl('/v2/users/register'), {
              method: "POST",
              headers: {
                'Content-Type': 'application/json',
              },
              credentials: 'include',
              body: JSON.stringify(payload),
            }).then((response) => {
              if(!response.ok) {
                // TODO handle more gracefully
                // or load 500 error page
                throw new Error('Failed to register user');
              }

            })

          }
          return token;
        },
        async signIn({ account, profile, user }) {
          return true;
          // if (profile?.email?.endsWith("@blackarrow.software") || 
          //     profile?.email?.endsWith("@helloomo.ai") ||
          //     profile?.email == "***REMOVED***") {
          //     return true; // true allows the user to signin
          // }
          // return false;
        }
    }
})