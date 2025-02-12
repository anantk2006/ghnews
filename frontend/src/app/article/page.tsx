"use client"; // Required for using hooks in the App Router

import { useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";
import Navbar from "../components/navbar";
import Footer from "../sections/footer";
import { motion } from "framer-motion";
import { useModal } from "../page";
import CheckoutForm from "../components/checkoutform";
import "../sections/modal.css";
import { div } from "framer-motion/client";

interface RelatedLink {
    [0]: string; // Title of the related article
    [1]: string; // URL of the related article
}

interface Article {
    title: string;
    content: string;
    related_links: RelatedLink[];
    pub_date: string;
}

export default function ArticlePage() {
    const searchParams = useSearchParams();
    const article_id = searchParams.get("id"); // Access the `id` query parameter
    const { isModalOpen, openModal, closeModal } = useModal();
    const [article, setArticle] = useState<Article | null>(null);
    

    useEffect(() => {
        const fetchArticle = async () => {
            try {
                const response = await fetch(`http://localhost:8000/api/article?id=${article_id}`, {
                    headers: {
                        "Content-Type": "application/json",
                        "Access-Control-Allow-Origin": "*",
                    },
                });
                const data = await response.json();                  
                setArticle(data);
                data.content = data.content.split('<br>').map((line: string, index: number) => (
                    <span key={index}>
                        { index == 0 ? (<div className="text-lg"><span className="text-6xl font-bold float-left mr-2">{line.charAt(0)}</span>
                        {line.slice(1)}</div> ) : (<span className="text-lg">{line}</span>)}
                    </span>
                  ));
                  
                console.log(data);
            } catch (error) {
                console.error("Error fetching article:", error);
            }
        };

        fetchArticle();
    }, [article_id]); // Dependency array ensures this runs only once when article_id changes
    
      
    return (
        <div className="min-h-screen flex flex-col">
            <Navbar openModal={openModal} />
            {isModalOpen && (
              <div className="modal-overlay" onClick={closeModal}>
                <div
                  className="modal-content"
                  onClick={(e) => e.stopPropagation()} // Prevent closing when clicking inside modal
                >
                  <button className="close-modal-button" onClick={closeModal}>
                    &times;
                  </button>
                  <CheckoutForm />
                </div>
              </div>
            )}
            <div className="flex-grow w-7/12 m-auto relative mb-10">
                <div className="flex flex-col items-center mt-10 gap-2 z-[99]">
                    <span className="text-4xl font-oddlini bg-clip-text text-purple-500">
                        {article ? article.title : ""}
                        
                    </span>
                    <span className="text-lg text-gray-500">{article ? article.pub_date : ""}</span>
                    <hr className="border-t-1 border-black w-full my-4" />
                    
                        {article ? article.content
                            
                         : (
                            "Loading..."
                        )}
                    
                    <hr className="border-t-1 border-black w-full my-4" />
                    <div className="flex flex-row w-full">
                        {article && typeof article === 'object' && 'related_links' in article && article.related_links.length > 0 && (
                            <div className="mt-8 w-full">
                                <h2 className="text-2xl font-bold mb-4 font-oddlini">Related Articles</h2>
                                <div className="flex flex-row flex-wrap w-full">
                                    {article.related_links.map((related: RelatedLink, index: number) => (
                                        <span key={index} className="text-black ml-4 mr-4 flex-1">
                                            <a href={related[1]} className="text-black hover:underline block text-center">
                                                {related[0]}
                                            </a>
                                        </span>
                                    ))}
                                </div>
                            </div>
                        )}
                    </div>
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.5, delay: 0.5 }}
                        className="group bg-white border-black/10 text-base text-black transition-all ease-in hover:cursor-pointer mb-4"
                    >
                    </motion.div>
                </div>
            </div>
            <Footer />
        </div>
    );
}