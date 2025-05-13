export default function AboutPage() {
    return (
        <main className="min-h-screen bg-gray-50 py-10 px-4">
            <div className="max-w-3xl mx-auto bg-white shadow-lg rounded-2xl p-8">
                <h1 className="text-2xl font-bold text-[#4A6EA9] mb-6">About the NGC Compressor</h1>
                
                <div className="space-y-4 text-gray-800 leading-relaxed">
                    <p>
                        The proposed compressor (NGC) is a reference-free, lossless, two-phase tool. Initially, it transforms the sequence into the primary domain of the DNA/RNA <span className="font-medium">{`{A, C, G, T/U}`}</span>, then proceeds with normalization. In the subsequent step, based on user specifications, it utilizes one of the eight general-purpose compressors, including 7-zip, paq8px, bsc, gzip, zstd, bzip2, zpaq, or cmix.
                    </p>
                </div>
            </div>
        </main>
    );
}
