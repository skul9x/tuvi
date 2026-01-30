"use client";

import { useEffect, useState, useRef } from "react";

interface ReadingStreamProps {
    dataJson: any;
    style: string;
}

export default function ReadingStream({ dataJson, style }: ReadingStreamProps) {
    const [content, setContent] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState("");
    const hasFetched = useRef(false);

    useEffect(() => {
        if (hasFetched.current) return;
        hasFetched.current = true;

        const fetchData = async () => {
            setIsLoading(true);
            setError("");
            setContent("");

            try {
                const response = await fetch("/api/chat", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                        data_json: dataJson,
                        style: style,
                    }),
                });

                if (!response.ok) {
                    throw new Error(response.statusText);
                }

                // Handle SSE Stream
                const reader = response.body?.getReader();
                const decoder = new TextDecoder();

                if (!reader) throw new Error("No reader available");

                while (true) {
                    const { done, value } = await reader.read();
                    if (done) break;

                    const chunk = decoder.decode(value);
                    const lines = chunk.split("\n\n");

                    for (const line of lines) {
                        if (line.startsWith("data: ")) {
                            const dataStr = line.replace("data: ", "");
                            if (dataStr === "[DONE]") {
                                setIsLoading(false);
                                return;
                            }
                            try {
                                const parsed = JSON.parse(dataStr);
                                if (parsed.text) {
                                    setContent((prev) => prev + parsed.text);
                                }
                            } catch (e) {
                                console.error("Parse error", e);
                            }
                        }
                    }
                }

            } catch (err) {
                setError("Lỗi kết nối AI: " + String(err));
            } finally {
                setIsLoading(false);
            }
        };

        if (dataJson) {
            fetchData();
        }
    }, [dataJson, style]);

    return (
        <div className="bg-white dark:bg-slate-900 p-6 rounded-lg shadow-lg border border-gray-200 dark:border-gray-800 min-h-[200px]">
            <h3 className="text-xl font-bold mb-4 text-purple-600 dark:text-purple-400 border-b pb-2">
                💎 Luận Giải AI ({style})
            </h3>

            <div className="prose dark:prose-invert max-w-none text-sm leading-relaxed whitespace-pre-wrap">
                {content}
            </div>

            {isLoading && (
                <div className="flex items-center gap-2 mt-4 text-gray-500 animate-pulse">
                    <span>✨ Đang luận giải thiên cơ...</span>
                </div>
            )}

            {error && (
                <div className="text-red-500 mt-4 p-4 bg-red-50 dark:bg-red-900/20 rounded">
                    {error}
                </div>
            )}
        </div>
    );
}
