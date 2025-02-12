import { cn } from "@/lib/utils";
import { Marquee } from "@/app/components/magic-marquee";

const reviews = [
  {
    articleName: "Deepseek R1 is released",
    datePublished: "February 8, 2025",
    tag: "AI news",
  },
  {
    articleName: "Deep research by Gemini",
    datePublished: "February 2, 2025",
    tag: "AI news",
  },
  {
    articleName: "Release of ChatGPT o3-mini",
    datePublished: "February 3, 2025",
    tag: "AI news",
  },
  {
    articleName: "Release of ChatGPT 3.5",
    datePublished: "January 2, 2025",
    tag: "AI news",
  },
  {
    articleName: "Release of Deepseek R1",
    datePublished: "January 1, 2025",
    tag: "AI news",
  },
  {
    articleName: "The Future of AI",
    datePublished: "January 7, 2025",
    tag: "AI news",
  },
];

const firstRow = reviews.slice(0, reviews.length / 2);
const secondRow = reviews.slice(reviews.length / 2);

const ReviewCard = ({
  articleName,
  datePublished,
  tag,
}: {
  articleName: string;
  datePublished: string;
  tag: string;
}) => {
  return (
    <figure
      className={cn(
        "relative h-32 w-80 cursor-pointer overflow-hidden rounded-xl border p-4",
      )}
    >
      <div className="flex flex-row items-center gap-2">
        <div className="flex flex-col">
          <figcaption className="text-md font-medium dark:text-white font-oddlini text-purple-500">
            {articleName}
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
  return (
    <div className="relative flex w-full flex-col items-center justify-center overflow-hidden mb-12">
      <Marquee pauseOnHover className="[--duration:10s]">
        {firstRow.map((review) => (
          <ReviewCard key={review.articleName} {...review} />
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
