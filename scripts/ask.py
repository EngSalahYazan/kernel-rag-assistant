from __future__ import annotations

from kernel_rag.bootstrap import build_pipeline


def main() -> None:
    pipeline = build_pipeline()
    print("Kernel Knowledge Assistant CLI")
    print("Type 'exit' to quit.\n")
    while True:
        question = input("You: ").strip()
        if question.lower() in {"exit", "quit"}:
            break
        if not question:
            continue
        response = pipeline.ask(question)
        print(f"\nAssistant: {response.answer}\n")
        for index, source in enumerate(response.sources, start=1):
            chunk = source.chunk
            page = chunk.page_start if chunk.page_start == chunk.page_end else f"{chunk.page_start}-{chunk.page_end}"
            print(
                f"  [{index}] {chunk.section} | {chunk.subsection or '-'} | "
                f"page {page} | similarity={source.similarity:.3f}"
            )
        print()


if __name__ == "__main__":
    main()
