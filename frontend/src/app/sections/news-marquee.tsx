import { cn } from "@/lib/utils";
import { Marquee } from "@/app/components/magic-marquee";
import { useEffect, useState } from "react";

type Review = {
    articleName: string;
    datePublished: string;
    tag: string;
    url: string;
};

const ReviewCard = ({
  articleName,
  datePublished,
  tag,
  url,
}: {
  articleName: string;
  datePublished: string;
  tag: string;
  url?: string;
}) => {
  return (
    <figure
      className={cn(
        "relative h-40 w-80 cursor-pointer overflow-hidden rounded-xl border p-4",
      )}
    >
      <div className="flex flex-row items-center gap-2">
        <div className="flex flex-col">
          <figcaption className="text-md font-medium dark:text-white font-oddlini text-purple-500">
            <a href={url}>
            {articleName}
            </a>
          </figcaption>
          <p className="text-sm dark:text-white/40 font-hanken font-bold mt-1">
            {datePublished}
          </p>
          <div className="rounded-full border border-purple-600/10 bg-purple-50/50 w-max px-4 py-1 text-left mt-2">
            <p className="text-xs font-medium text-purple-600 font-hanken">
              {tag}
            </p>
          </div>
        </div>
      </div>
    </figure>
  );
};

export function NewsMarquee() {
  const [reviews, setReviews] = useState<Review[]>([]);

  useEffect(() => {
    fetch("https://api.virsitile.dev/api/recents",
        { method: "GET", headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*", } }
    )
      .then((response) => response.json())
      .then((data) => setReviews(data))
      .catch((error) => console.error("Error fetching reviews:", error));
  }, []);

  const firstRow = reviews.slice(0, reviews.length / 2);
  const secondRow = reviews.slice(reviews.length / 2);

  return (
    <div className="relative flex w-full flex-col items-center justify-center overflow-hidden mb-12">
        <h1 className="font-oddlini mb-7 text-3xl">Today's Articles</h1>
      <Marquee pauseOnHover className="[--duration:10s]">
        {firstRow.map((review) => (
            (review ? <ReviewCard key={review.articleName} {...review} /> : "")
        ))}
      </Marquee>
      <Marquee reverse pauseOnHover className="[--duration:10s]">
        {secondRow.map((review) => (
          <ReviewCard key={review.articleName} {...review} />
        ))}
      </Marquee>
      <div className="pointer-events-none absolute inset-y-0 left-0 w-1/4 bg-gradient-to-r from-background"></div>
      <div className="pointer-events-none absolute inset-y-0 right-0 w-1/4 bg-gradient-to-l from-background"></div>
    </div>
  );
}