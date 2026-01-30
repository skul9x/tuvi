export type Json =
    | string
    | number
    | boolean
    | null
    | { [key: string]: Json | undefined }
    | Json[]

export interface Database {
    public: {
        Tables: {
            profiles: {
                Row: {
                    id: string
                    email: string
                    full_name: string | null
                    avatar_url: string | null
                    updated_at: string | null
                }
                Insert: {
                    id: string
                    email: string
                    full_name?: string | null
                    avatar_url?: string | null
                    updated_at?: string | null
                }
                Update: {
                    id?: string
                    email?: string
                    full_name?: string | null
                    avatar_url?: string | null
                    updated_at?: string | null
                }
            }
            saved_horoscopes: {
                Row: {
                    id: string
                    user_id: string
                    name: string
                    dob_solar: string
                    dob_lunar: string
                    gender: number
                    created_at: string
                    data_json: Json
                }
                Insert: {
                    id?: string
                    user_id: string
                    name: string
                    dob_solar: string
                    dob_lunar: string
                    gender: number
                    created_at?: string
                    data_json: Json
                }
                Update: {
                    id?: string
                    user_id?: string
                    name?: string
                    dob_solar?: string
                    dob_lunar?: string
                    gender?: number
                    created_at?: string
                    data_json?: Json
                }
            }
        }
        Views: {
            [_ in never]: never
        }
        Functions: {
            [_ in never]: never
        }
        Enums: {
            [_ in never]: never
        }
        CompositeTypes: {
            [_ in never]: never
        }
    }
}
