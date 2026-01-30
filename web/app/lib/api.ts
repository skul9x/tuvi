export interface HoroscopeRequest {
    name: string;
    day: number;
    month: number;
    year: number;
    hour: number;
    gender: number;
    viewing_year?: number;
}

export interface HoroscopeResponse {
    info: any;
    cung: any[];
    scores: any;
}

export const api = {
    ansao: async (data: HoroscopeRequest): Promise<HoroscopeResponse> => {
        const res = await fetch("/api/ansao", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });

        if (!res.ok) {
            const errorData = await res.json().catch(() => ({}));
            console.error("API Error Details:", errorData, res.status, res.statusText);
            throw new Error(errorData.error || `Server Error (${res.status}): ${res.statusText}`);
        }

        return res.json();
    },

    // Chat endpoint is streaming, so it's usually handled differently (fetch + getReader), 
    // but we can add a helper url generator or headers here if needed.
    chatUrl: "/api/chat"
};
